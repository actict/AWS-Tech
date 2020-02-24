#!/usr/bin/env python3
# create_sg_hashivault.py
#
# Last Updated: 2018.12.09
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to create a security group for EC2 instance
# 'hashi_vault' and adds ingress rules to this security group. Finally,
# it adds this security group to 'hashi_vault'

import boto3
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


session = boto3.Session(profile_name = 'prod')
ec2Resource = session.resource('ec2')
ec2Client = session.client('ec2')

resp = ec2Resource.create_security_group(
    GroupName = 'sg_hashivault',
    Description = 'Security Group for Hashicorp Vault',
    VpcId = vpc_gdac)

check_response_status(resp)

resp1 = ec2Client.authorize_security_group_ingress(
    GroupId = sg_hashivault,
    IpPermissions=[
        {
            'FromPort': 8200,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': '10.0.0.0/16',
                    'Description': 'Vault listener'
                },
            ],
            'ToPort': 8200,
        },
        {
            'FromPort': 8125,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': '10.0.0.0/16',
                    'Description': 'Vault telemetry'
                },
            ],
            'ToPort': 8125,
        },
    ],
)

check_response_status(resp1)

resp2 = ec2Client.modify_network_interface_attribute(
    Groups = [
        sg_hashivault,
        sg_ssh_from_zpa_connector,
    ],
    NetworkInterfaceId = eni_hashivault
)

check_response_status(resp2)
