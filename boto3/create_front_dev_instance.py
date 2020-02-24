#!/usr/bin/env python3
# create_front_dev_instance.py
#
# Last Updated: 2018.09.28
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance to be used
# as a front-dev web server complete with necessary Security
# Groups, subnets, ssh key, root disk size, IAM Role, and custom
# tags.

# Notes:
# 'ami-012566705322e9a8e' is the AMI for
# 'amzn2-ami-hvm-2.0.20180810-x86_64-gp2' which is the lastest
# Amazon Linux 2 image as of 09.28
# SG is 'styleket'
# Subnet is '2a-subnet-bogeup-VPC'


import boto3


session = boto3.Session(profile_name = 'dev')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')

print("### Creating front-dev instance... ###")
instance = ec2Resource.create_instances(
    ImageId = "ami-012566705322e9a8e",
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.small',
    IamInstanceProfile = {
    'Arn': 'arn:aws:iam::905136931838:instance-profile/phoenix-cw-collectd-dev'
    },
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                 'VolumeSize': 30
            }
        }
    ],
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': 'subnet-cfb5d0a7',
            'Groups': ['sg-559bf03e'],
            'AssociatePublicIpAddress': True
        }
    ],
    KeyName = 'dev-styleket'
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
            'Value': 'miriya'
        },
        {
            'Key': 'Name',
            'Value': 'front-dev-new-A'
        },
    ]
)
