#!/usr/bin/env python3
# prod_affogatolb_revoke_sg.py
#
# Last Updated: 2018.11.28
# Updated by: hulk.choi@actwo.com
#
# This script revokes ALL ingress rules from the Security Group
# for Prod affogato Load Balancer for Elastic Beanstalk.


import boto3
from env_prod import *

session = boto3.Session(profile_name = 'prod')

ec2Client = session.client('ec2')

resp=ec2Client.revoke_security_group_ingress(
    GroupId = 'sg_prod_affogato_lb',
    IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                   {
                       'CidrIp':any,
                   },
                           ],
               'ToPort': 80,
            },
    ],
)

print(resp)
