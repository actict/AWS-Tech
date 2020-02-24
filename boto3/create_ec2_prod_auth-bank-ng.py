#!/usr/bin/env python3
# create_ec2_prod_auth-bank-ng.py
#
# Last Updated: 2019.10.21
# Updated by: jun.go@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# for auth-bank-ng (new generation) in AWS PROD to replace
# auth-bank-new which has a problem with Java updates due env
# vars. This server allows TCP ports 80, 8080, 8081 from the VPC IP
# range 10.0.0.0/16 and TCP 22 from the wireguard VPN server.


import boto3
import time
from env_ami import ami_amzn_linux2_gp2
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
    my_inst_name = 'gdac-prod-exchange-auth-bank-ng'

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
            }
        ],
        NetworkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': subnet_dict['auth-bank-phone-2a'],
                'Groups': [
                    sec_group_dict['auth-bank'],
                    sec_group_dict['wireguard-ssh']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['auth-bank-ng'],
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
                    'Value': 'kyle'
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
