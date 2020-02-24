#!/usr/bin/env python3
# create_ec2_admin_all.py
#
# Last Updated: 2018.12.12
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as a admin-front and admin-access.

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
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    my_inst_name = 'gdac-prod-exchange-admin' # basename to give to new EC2's

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 2,
        MaxCount = 2,
        InstanceType = 't3.small',
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
                'SubnetId': sub_pri_admin_2a,
                'Groups': [
                    sg_default_admin_net,
                    sg_wg_ssh,
                    sg_wg_http,
                    sg_wg_https
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = 'phoenix-admin',
        DryRun = False
    )

    for i in range(len(instance)):
        print("### Adding name and owner tags to instance %s ###"
              %instance[i].id)
        instance_name = my_inst_name + '-' + str(i)
        resp = client.create_tags(
            DryRun = False,
            Resources = [
                instance[i].id
            ],
            Tags = [
                {
                    'Key': 'owner',
                    'Value': 'henry'
                },
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
                {
                    'Key': 'Account',
                    'Value': 'GDAC'
                },
                {
                    'Key': 'fqdn',
                    'Value': 'adm.gdac.com, api-adm.gdac.com'
                },
            ]
        )
        check_response_status(resp)


if __name__ == "__main__":
    main()
