#!/usr/bin/env python3
# create_ec2_auth_bank.py
#
# Last Updated: 2019.01.10
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# to replace Elastic Beanstalk auth-bank

import boto3
import time
from env_ami import *
from env_prod import *


def check_response_status(mydict):
    """
    dict, string -> string to stdout

    Given a dict containing the HTTP Status Code response of a boto3
    request, print to stdout depending on the HTTP Status Code value
    """
    if mydict['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("creation SUCCESS")
    else:
        print("creation ERROR")


def main():
    session = boto3.Session(profile_name = 'prod')
    ec2Client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    my_inst_name = 'auth-bank' # basename to give to new EC2's

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.micro',
        IamInstanceProfile = {
            'Arn' : iam_phoenix_collectd
        },
        BlockDeviceMappings = [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 20,
                    'VolumeType': 'gp2'
                }
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': sub_pri_auth_bank_phone_2a,
                'Groups': [
                    sg_ssh_from_zpa_connector,
                    sg_auth_bank_new
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_auth_bank,
        DryRun = False
    )

    for i in range(len(instance)):
        print("### Adding name and owner tags to instance %s ###"
              %instance[i].id)
        instance_name = my_inst_name + '-' + str(i)
        resp = ec2Client.create_tags(
            DryRun = False,
            Resources = [
                instance[i].id
            ],
            Tags = [
                {
                    'Key': 'owner',
                    'Value': 'hank'
                },
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        )
        check_response_status(resp)

        print("Sleep for 30 sec to allow the instance to come up...")
        time.sleep(30)
        print("Allocating permanent Elastic IP...")
        allocation = ec2Client.allocate_address(Domain = 'vpc')
        print("Associate new Elastic IP with EC2 instance")
        response = ec2Client.associate_address(
            AllocationId=allocation['AllocationId'],
            InstanceId=instance[i].id,
            AllowReassociation=True
        )
        check_response_status(response)


if __name__ == "__main__":
    main()
