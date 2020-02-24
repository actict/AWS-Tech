#!/usr/bin/env python3

# revoke_new_office_to_aws.py
#
# Last Updated: 2019.2.15
# Created by: joshua.huh@actwo.com
#
# Purpose: allow access from new office to access server

import boto3
from env_prod import *

session = boto3.Session(region_name = 'ap-northeast-2', profile_name = 'prod')
ec2Client = session.client('ec2')

target = [ sg_zscaler_connector, sg_bitgo_interface_service, sg_wireguard_PROD ]

for i in target:
    req = ec2Client.revoke_security_group_ingress(

        GroupId = i,
        IpPermissions = [
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [{ 'CidrIp': cidr_office_actwo }],
                'ToPort': 22,
            }
        ]
    )

    print(req)
