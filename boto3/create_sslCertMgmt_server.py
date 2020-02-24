#!/usr/bin/env python3
# create_sslCertMgmt_server.py
#
# Last Updated: 2018.10.19
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance to be used
# as SSL cert mgmt server complete with necessary Security
# Groups, subnets, ssh key, root disk size, IAM Role, and custom
# tags. This server will automatically renew Let's Encrypt SSL
# certificates in use throughout the Actwo infrastructure

# Notes:
# 'ami-0b04c9bf8abfa5b89' is the latest Ubuntu 18.04 LTS AMI as of
# 2018.10.12. The subnet is "dmz-management-2a", i.e.,
# "subnet-0fea3d7e77bde6b89". The Security Group is "wireguard-ssh"
# i.e., "sg-018e0e0b78b4b8322"


import boto3


session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    ImageId = 'ami-0b04c9bf8abfa5b89',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.nano',
    IamInstanceProfile = {
    'Arn': 'arn:aws:iam::762015387773:instance-profile/phoenix-cw-collectd'
    },
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                 'VolumeSize': 10
            }
        }
    ],
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': 'subnet-0fea3d7e77bde6b89',
            'Groups': ['sg-018e0e0b78b4b8322'],
            'AssociatePublicIpAddress': True
        }
    ],
    KeyName = 'phoenix-back-common'
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
            'Value': 'PJ'
        },
        {
            'Key': 'Name',
            'Value': 'ssl-cert-mgmt'
        },
    ]
)
