#!/usr/bin/env python3
# create_ec2_candy_with_eip.py
#
# Last Updated: 2018.11.26
# Updated by: joshua.huh@actwo.com
#
# This script uses boto3 to create EC2 instance(s) with elastic IP address(es).

import boto3
import time
from env_candy import *


session = boto3.Session(profile_name = 'candy')
client = session.client('ec2')
ec2Resource = session.resource('ec2')
my_inst_name = 'candy' # basename to give to new EC2's

print("### Creating instance... ###")
instance = ec2Resource.create_instances(
    ImageId = ami_ubuntu_1804,
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't3.small',
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                 'VolumeSize': 20
            }
        }
    ],
    NetworkInterfaces = [
        {
            'DeviceIndex': 0,
            'SubnetId': subnet_dmz,
            'Groups': [sg_candy_beanstalk, sg_candy_deploy_group, sg_candy_sandbox_candy_crawler, sg_candy_candy_control ],
            'AssociatePublicIpAddress': False
        }
    ],
    KeyName = ssh_candy,
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
                'Value': 'jayce'
            },
            {
                'Key': 'Name',
                'Value': instance_name
            },
        ]
    )

    time.sleep(30)
    allocation = client.allocate_address(Domain = 'vpc')
    response = client.associate_address(
        AllocationId=allocation['AllocationId'],
        InstanceId=instance[i].id,
        AllowReassociation=True
    )