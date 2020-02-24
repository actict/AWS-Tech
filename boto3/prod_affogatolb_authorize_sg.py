#!/usr/bin/env python3
# prod_affogatolb_authorize_sg.py
#
# Last Updated: 2018.11.28
# Updated by: hulk.choi@actwo.com
#
# This script adds ALL ingress rules from the Security Group
# for Prod affogato Load Balancer for Elastic Beanstalk.


import boto3
from env_prod import *

session = boto3.Session(profile_name = 'prod')

ec2Client = session.client('ec2')

resp=ec2Client.authorize_security_group_ingress(
    GroupId = sg_prod_affogato_lb,
    IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                   {
                       'CidrIp': zia_office,
                   },
                           ],
               'ToPort': 80,
            },
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                   {
                       'CidrIp': nat_2a,
                   },
                           ],
               'ToPort': 80,
            },
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                   {
                       'CidrIp': nat_dmz_access,
                   },
                           ],
               'ToPort': 80,
            },
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                   {
                       'CidrIp': nat_2c,
                   },
                           ],
               'ToPort': 80,
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'UserIdGroupPairs': [{ 'GroupId': sg_prod-access }] },

           # {
           #     'IpProtocol': 'tcp',
           #     'FromPort': 80,
           #     'ToPort': 80,
           #     'UserIdGroupPairs': [{ 'GroupId': 'sg-07e2ef27cdc1e4b4d' }] },
    ],
)

print(resp)
