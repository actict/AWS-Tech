#!/usr/bin/env python3

'''
revoke_ingress_to_partner_lb.py

Last Updated: 2019.10.21
Created by: joshua.huh@actwo.com
Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com

Purpose: revoke ingress traffic to partnerAPI LB and set
LB idle_timeout to 1 sec to cut off in-flight connections'
'''


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['partner-api']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '1'
        },
    ]
)

print("### Results of changing partner.gdac.com LB idle timeout to 1 sec ###")
print(resp)

time.sleep(1)

resp1 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['partner-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [{'CidrIp': cidr_dict['any-ip']}],
            'Ipv6Ranges': [{'CidrIpv6': cidr_dict['any-ip6']}],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [{'CidrIp': cidr_dict['any-ip']}],
            'Ipv6Ranges': [{'CidrIpv6': cidr_dict['any-ip6']}],
            'ToPort': 443
        }
    ],
    # DryRun = True
)

print("### Results of revoking ingress SG of partner.gdac.com LB ###")
print(resp1)

time.sleep(1)

resp2 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['partner'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['partner-lb'],
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    #DryRun = True
)

print("### Results of revoking ingress SG to partnerAPI server ###")
print(resp2)

time.sleep(5)

resp3 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['partner'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['partner-lb'],
                    'Description': 'http via LB',
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    #DryRun = True
)

print("### Results of authorizing ingress SG to partnerAPI server ###")
print(resp3)
