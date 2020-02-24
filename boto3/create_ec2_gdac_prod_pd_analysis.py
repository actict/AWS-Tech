#!/usr/bin/env python3
# create_ec2_gdac_prod_pd_analysis.py
#
# Last Updated: 2019.03.08
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create an EC2 instance that will be used
# as an analysis and batch server in the PROD envo for the Product
# Development team. This server can connect to AuroraDB PROD and also
# allows connections on TCP 3306. This server does not accept Internet
# traffic.


import boto3
import time
from env_ami import ami_amzn_linux2_gp2
from env_prod import *


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
    my_inst_name = 'gdac-prod-exchange-PD-analysis'

    print("### Creating instance... ###")
    instance = ec2Resource.create_instances(
        ImageId = ami_amzn_linux2_gp2,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't3.small',
        IamInstanceProfile = {
            'Arn' : iam_phoenix_collectd
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
                'SubnetId': sub_pri_ledger_2a,
                'Groups': [
                    sg_pd_node,
                    sg_ssh_from_zpa_connector
                ],
                'AssociatePublicIpAddress': False
            }
        ],
        KeyName = ssh_pd_node,
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
                    'Value': 'PD node'
                },
                {
                    'Key': 'Account',
                    'Value': 'GDAC'
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
