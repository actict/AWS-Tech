#!/usr/bin/env python3
# create_ec2_cosmos_testnet.py
#
# Last Updated: 2019.04.17
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as a COSMOS fullnode for gaia testnets in DEV mainnet.


import boto3
import time
from env_ami import ami_ubuntu_1804
from env_dev import *


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
    start = time.time()
    session = boto3.Session(profile_name = 'dev')
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    # basename to give to new EC2's
    my_inst_name = 'gdac-devmain-cosmos-testnet'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_ubuntu_1804,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.large',
        IamInstanceProfile = {
            'Arn' : iam_collectd_cw_dev
        },
        BlockDeviceMappings = [
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 20,
                    'VolumeType': 'gp2'
                }
            },
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 1024,
                    'VolumeType': 'gp2'
                }
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_pri_2a,
                'Groups': [
                    sg_cosmos_devmain,
                    sg_cosmos_and_wallet,
                    sg_wireguard_dev_ssh
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_dev_real_private,
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
                    'Value': 'ted'
                },
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        )
        check_response_status(resp)
    end = time.time()
    print("This script ran in %s seconds." %(end - start))


if __name__ == "__main__":
    main()
