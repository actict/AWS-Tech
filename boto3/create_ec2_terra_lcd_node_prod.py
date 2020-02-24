#!/usr/bin/env python3
# create_ec2_terra_full_node_prod.py
#
# Last Updated: 2019.05.14
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as a Terra mainnet light client node in AWS PROD envo. This server
# needs to be able to communicate on TCP 1317 (light client port) and
# TCP 6015 (wallet svr).


import boto3
import time
from env_ami import ami_ubuntu_1804
from env_prod import subnet_dict, sec_group_dict
from env_prod import iam_profile_dict, ssh_keys_dict


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
    session = boto3.Session(profile_name = 'prod')
    client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    my_inst_name = 'gdac-prod-exchange-terra-lcd'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_ubuntu_1804,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.micro',
        IamInstanceProfile = {
            'Arn': iam_profile_dict['collectd']
        },
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
                'SubnetId': subnet_dict['gdac-priv-2a'],
                'Groups': [
                    sec_group_dict['wireguard-ssh'],
                    sec_group_dict['wallet-terra'],
                    sec_group_dict['common-lcd']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['wallet'],
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
                    'Value': 'hank, ted'
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
