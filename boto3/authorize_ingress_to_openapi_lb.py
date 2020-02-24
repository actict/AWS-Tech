#!/usr/bin/env python3

'''
authorize_ingress_to_openapi_lb.py

Last Updated: 2019.10.24
Updated by: scott.hwang@peertec.com, joshua.huh@actwo.com

Purpose: allow ingress traffic to openAPI LB and set LB
idle timeout back to 60 sec.
'''


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp1 = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['openapi']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '60'
        },
    ]
)

time.sleep(1)

resp2 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['openapi-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': cidr_dict['candy-crawler'],
                    'Description': 'candy-crawler'
                },
                {
                    'CidrIp': cidr_dict['candy-crawler-orderbook'],
                    'Description': 'candy-crawler-orderbook'
                },
                {
                    'CidrIp': cidr_dict['candy-crawler-price'],
                    'Description': 'candy-crawler-price'
                },
                {
                    'CidrIp': cidr_dict['candy-db-redis'],
                    'Description': 'candy-db-redis, USELESS, maybe'
                },
                {
                    'CidrIp': cidr_dict['candy-deploy'],
                    'Description': 'candy-deploy, USELESS, maybe'
                },
                {
                    'CidrIp': cidr_dict['candy-halls'],
                    'Description': 'candy-halls'
                },
                {
                    'CidrIp': cidr_dict['candy-halls-cow'],
                    'Description': 'candy-halls-cow'},
                {
                    'CidrIp': cidr_dict['candy-ricola'],
                    'Description': 'candy-ricola'
                },
                {
                    'CidrIp': cidr_dict['office'],
                    'Description': 'our office'
                },
                {
                    'CidrIp': cidr_dict['pecunian-tokyo'],
                    'Description': 'pecunian-tokyo'
                }
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': cidr_dict['candy-crawler'],
                    'Description': 'candy-crawler'
                },
                {
                    'CidrIp': cidr_dict['candy-crawler-orderbook'],
                    'Description': 'candy-crawler-orderbook'
                },
                {
                    'CidrIp': cidr_dict['candy-crawler-price'],
                    'Description': 'candy-crawler-price'
                },
                {
                    'CidrIp': cidr_dict['candy-db-redis'],
                    'Description': 'candy-db-redis, USELESS, maybe'
                },
                {
                    'CidrIp': cidr_dict['candy-deploy'],
                    'Description': 'candy-deploy, USELESS, maybe'
                },
                {
                    'CidrIp': cidr_dict['candy-halls'],
                    'Description': 'candy-halls'
                },
                {
                    'CidrIp': cidr_dict['candy-halls-cow'],
                    'Description': 'candy-halls-cow'},
                {
                    'CidrIp': cidr_dict['candy-ricola'],
                    'Description': 'candy-ricola'
                },
                {
                    'CidrIp': cidr_dict['office'],
                    'Description': 'our office'
                },
                {
                    'CidrIp': cidr_dict['pecunian-tokyo'],
                    'Description': 'pecunian-tokyo'
                }
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)


print("### Results of changing openapi LB idle timeout to 60 sec ###")
print(resp1)

print("### Results of opening SG ingress for openapi lb ###")
print(resp2)

