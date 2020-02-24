#!/usr/bin/env python3
# create_ec2_hdac.py
#
# Last Updated: 2019.03.13
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance to be used
# as an HDAC blockchain server complete with necessary Security
# Groups, subnets, ssh key, root disk size, IAM Role, and custom
# tags.
#
# Note -- the BlockDeviceMappings in this file are incorrect;
# a root disk of 500GB was NOT created by this script!!! Instead
# a STANDARD magnetic disk was created...


import boto3
from env_ami import *
from env_dev import *

session = boto3.Session(profile_name = 'dev')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    # Ubuntu 16.04 LTS hvm:ebs-ssd
    ImageId = ami_ubuntu_1604,
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't3.medium',
    IamInstanceProfile = {
    'Arn': iam_phoenix_collectd
    },
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                 'VolumeSize': 500
            }
        }
    ],
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': pri_2a_subnet,
            'Groups': [sg_wireguard_mainnet, sg_default_private],
            'AssociatePublicIpAddress': False
        }
    ],
    KeyName = key_dev_generic,
    DryRun = False
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
            'Value': 'Ted'
        },
        {
            'Key': 'Name',
            'Value': 'hdac-mainnet'
        },
    ]
)
