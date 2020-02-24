#!/usr/bin/env python3
# create_ec2_prod_hashtower.py
#
# Last Updated: 2019.06.11
# Updated by: joshua.huh@actwo.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as an irisnet light client (LCD) in gdac PROD envo.


import boto3
import time
from env_ami import ami_amzn_linux2_gp2
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
    # basename to give to new EC2's
    my_inst_name = 'hashtowoer-prod-web'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.nano',
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
                'SubnetId': subnet_dict['peer-pri-2a'],
                'Groups': [
                    sec_group_dict['wireguard-peer-ssh'],
                    sec_group_dict['hashtower-web']
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_keys_dict['hashtower'],
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
                    'Key': 'fqdn',
                    'Value': 'www.hashtower.com'
                },
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
                {
                    'Key': 'Account',
                    'Value': 'HASHTOWER'
                }
            ]
        )
        check_response_status(resp)
    end = time.time()
    print("This script ran in %s seconds." %(end - start))


if __name__ == "__main__":
    main()
