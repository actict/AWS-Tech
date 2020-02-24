#!/usr/bin/env python3

'''
authorize_ingress_to_partner_lb.py

Created by: joshua.huh@actwo.com
Last Updated: 2019.10.30
Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com

Purpose: allow ingress traffic to partnerAPI LB and set
LB idle_timeout back to default of 60 sec to allow traffic
'''


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp1 = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['partner-api']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '60'
        },
    ]
)

time.sleep(1)

resp2 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['partner-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': cidr_dict['any-ip'],
                    'Description': 'access to partner.gdac.com'
                }
            ],
            'Ipv6Ranges': [
                {
                    'CidrIpv6': cidr_dict['any-ip6'],
                    'Description': 'access to partner.gdac.com'
                }
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': cidr_dict['any-ip'],
                    'Description': 'access to partner.gdac.com'
                }
            ],
            'Ipv6Ranges': [
                {
                    'CidrIpv6': cidr_dict['any-ip6'],
                    'Description': 'access to partner.gdac.com'
                }
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)

print("### Results of changing LB idle timeout to 60 sec ###")
print(resp1)

print("### Results of revoking SG ingress ###")
print(resp2)
