#!/usr/bin/env python3
# create_ec2_prod_front.py
#
# Last Updated: 2018.12.12
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as the front web server for gdac.com

import boto3
import time
from env_ami import ami_amzn_linux2_gp2
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
    my_inst_name = 'prod-front' # basename to give to new EC2's

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 6,
        MaxCount = 6,
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
                'SubnetId': sub_dmz_front_auth_kakao_2a,
                'Groups': [
                    sg_gdac_front,
                    sg_ssh_from_zpa_connector
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = 'phoenix-front',
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
                    'Value': 'miriya'
                },
                {
                    'Key': 'Account',
                    'Value': 'GDAC'
                },
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        )
        check_response_status(resp)


if __name__ == "__main__":
    main()
