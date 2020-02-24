#!/usr/bin/env python3
# create_hexlant_prod.py
#
# Last Updated: 2018.11.05
# Updated by: scott.hwang@peertec.com, hulk.choi@actwo.com
#
# This script uses boto3 to create 3 EC2 instances to be used
# as DPOS validators by Hexcellent.


import boto3
from env_ops import *


session = boto3.Session(profile_name = 'ops')
ec2Client = session.client('ec2')
ec2Resource = session.resource('ec2')
my_inst_name = 'hexlant' # basename to give to new EC2's

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    ImageId = ami_ubu_1604,
    MinCount = 3,
    MaxCount = 3,
    InstanceType = 'm5.large',
    IamInstanceProfile = {
    'Arn': iam_profile
    },
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                 'VolumeSize': 20
            }
        },
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                 'VolumeType': 'io1',
                 'Iops': 5000,
                 'VolumeSize': 100
            }
        }
    ],
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': hexlant_subnet,
            'Groups': [sg_prod_wallet_hexlant],
            'AssociatePublicIpAddress': True
        }
    ],
    KeyName = ssh_hexlant
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
