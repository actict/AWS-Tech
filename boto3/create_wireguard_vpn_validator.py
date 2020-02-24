#!/usr/bin/env python3
# create_wireguard_vpn_validator.py
#
# Last Updated: 2018.11.02
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance to be used
# as a wireguard VPN server complete with necessary Security
# Groups, subnets, ssh key, root disk size, IAM Role, and custom
# tags. This server will provide VPN access to instances in validator
# VPC and subnets.


import boto3
from env_validator import *


session = boto3.Session(profile_name = 'validator')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')
my_inst_name = 'wireguard-server' # basename to give to new EC2's

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    ImageId = ami_ubu_1804,
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.nano',
    IamInstanceProfile = {
    'Arn': iam_profile
    },
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': public_subnet,
            'Groups': [sg_wireguard_udp, sg_ssh_to_vpn],
            'AssociatePublicIpAddress': True
        }
    ],
    KeyName = ssh_wireguard_vali
)

for i in range(len(instance)):
    print("### Adding name and owner tags to instance %s ###"
          %instance[i].id)
    myname = my_inst_name + '_' + str(i)
    resp = ec2Client.create_tags(
        DryRun = False,
        Resources = [
            instance[i].id
        ],
        Tags = [
            {
                'Key': 'owner',
                'Value': 'pj'
            },
            {
                'Key': 'Name',
                'Value': myname
            },
        ]
    )
