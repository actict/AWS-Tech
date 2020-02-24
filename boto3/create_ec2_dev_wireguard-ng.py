#!/usr/bin/env python3
# create_ec2_dev_wireguard-ng.py
#
# Last Updated: 2019.11.05
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# for peerpay orderbot in AWS DEV. Note that for Ubuntu 18.04 AMI
# using gp2 ssd, the root disk will always use /dev/sda1 device name
# while non-root disks use /dev/xvdY format. This server will also
# communicate with AuroraDB on TCP 3306. In addition, TCP 5000 and 80
# should be accessible from the Wireguard VPN server and the VPC
# internal subnets.


import boto3
import time
from env_ami import ami_ubuntu_1804
from env_dev import subnet_dict, iam_profile_dict, sec_group_dict
from env_dev import ssh_keys_dict


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
    session = boto3.Session(profile_name = 'dev_ec2_full')
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    # basename to give to new EC2's
    my_inst_name = 'gdac-devtest-wireguard-ng'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_ubuntu_1804,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.micro',
        IamInstanceProfile = {
            'Arn' : iam_profile_dict['collectd']
        },
        BlockDeviceMappings = [
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 20,
                    'VolumeType': 'gp2'
                }
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_dict['testnet-2a'],
                'Groups': [
                    sec_group_dict['wireguard-ng-testnet']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['connector'],
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
                    'Value': 'james'
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
