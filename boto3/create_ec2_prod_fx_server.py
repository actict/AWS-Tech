#!/usr/bin/env python3
# create_ec2_prod_fx_server.py
#
# Last Updated: 2019.09.30
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as an exchange rate server in AWS PROD. Jenkins is able to access
# the server via TCP 22 and the server also communicates with AuroraDB
# on TCP 3306. In addition, TCP 3000 should be accessible from the
# Wireguard VPN server and 5011 should be accessible from the
# porsche-api SG.

# Note that for ubuntu using gp2 ssd, the root disk will always use
# /dev/sda1 device name while non-root disks use /dev/xvdY format.


import boto3
import time
from env_ami import ami_ubuntu_1804
from env_prod import subnet_dict, iam_profile_dict, sec_group_dict
from env_prod import ssh_keys_dict


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
    session = boto3.Session(profile_name = 'prod_ec2_full')
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    # basename to give to new EC2's
    my_inst_name = 'gdac-prod-exchange-fx'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_ubuntu_1804,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.small',
        IamInstanceProfile = {
            'Arn' : iam_profile_dict['collectd']
        },
        BlockDeviceMappings = [
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 40,
                    'VolumeType': 'gp2'
                }
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_dict['gdac-priv-2a'],
                'Groups': [
                    sec_group_dict['allow-jenkins-ssh'],
                    sec_group_dict['auroradb'],
                    sec_group_dict['fx'],
                    sec_group_dict['wireguard-ssh']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['fx'],
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
                    'Value': 'luke'
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
