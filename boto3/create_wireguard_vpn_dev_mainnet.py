#!/usr/bin/env python3
# create_wireguard_vpn_dev_mainnet.py
#
# Last Updated: 2018.10.24
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance to be used
# as a wireguard VPN server complete with necessary Security
# Groups, subnets, ssh key, root disk size, IAM Role, and custom
# tags. This server will provide VPN access to instances in DEV mainnet
# VPC and subnets.
#
# Notes:
# 'ami-0b04c9bf8abfa5b89' is the latest Ubuntu 18.04 LTS AMI as of
# 2018.10.12. The subnet is "public-2a-fe", i.e.,
# "subnet-06739379b072cd86e". The Security Groups are "zpa-connector"
# ("sg-073c0e28200ffcbb1") and "wireguard-mainnet-sg"
# ("sg-06bca0ac5a54b0d50")


import boto3


session = boto3.Session(profile_name = 'dev')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    ImageId = 'ami-0b04c9bf8abfa5b89',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.nano',
    IamInstanceProfile = {
    'Arn': 'arn:aws:iam::905136931838:instance-profile/phoenix-cw-collectd-dev'
    },
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': 'subnet-06739379b072cd86e',
            'Groups': ['sg-073c0e28200ffcbb1', 'sg-06bca0ac5a54b0d50'],
            'AssociatePublicIpAddress': True
        }
    ],
    KeyName = 'connector'
)

instanceid = instance[0].id

print("### Adding name and owner tags to created instance... ###")

resp = ec2Client.create_tags(
    DryRun = False,
    Resources = [
        instanceid
    ],
    Tags = [
        {
            'Key': 'owner',
            'Value': 'pj'
        },
        {
            'Key': 'Name',
            'Value': 'wireguard-mainnet'
        },
    ]
)
