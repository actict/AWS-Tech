#!/usr/bin/env python3
# create_ec2_hashicorp_vault_dev.py
#
# Last Updated: 2019.05.27
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as a Hashicorp Vault server in AWS DEV. Note that for Amazon Linux 2
# AMI using gp2, the root disk will always use /dev/xvda device name
# while non-root disks use /dev/sdxy format. So this script sets root
# disk of 20GB, secondary disk of 10GB.


import boto3
import time
from env_ami import ami_amzn_linux2_gp2
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
    session = boto3.Session(profile_name = 'dev_eb_ec2_full')
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    # basename to give to new EC2's
    my_inst_name = 'gdac-dev-hashicorp-vault'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.micro',
        IamInstanceProfile = {
            'Arn' : iam_profile_dict['collectd']
        },
        BlockDeviceMappings = [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'VolumeSize': 20,
                    'VolumeType': 'gp2'
                }
            },
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 10,
                    'VolumeType': 'gp2'
                }
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_dict['private-2a'],
                'Groups': [
                    sec_group_dict['hashivault'],
                    sec_group_dict['wireguard-ssh']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['private'],
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
                    'Value': 'larry'
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
