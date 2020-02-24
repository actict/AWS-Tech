#!/usr/bin/env python3

'''
revoke_ingress_to_openapi_lb.py

Last Updated: 2019.10.21
Updated by: scott.hwang@peertec.com, joshua.huh@actwo.com

Purpose: revoke ingress traffic to openAPI LB and set the LB
idle timeout to 1s to cut off connections in-flight

Revoking ingress traffic in LB is NOT enough!!!
Even minimum idle timeout is too long to clear all in-flight
sessions. Temporary traffic choking in the server is required.
'''


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['openapi']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '1'
        },
    ]
)

print("### Results of changing openapi LB idle timeout to 1 sec ###")
print(resp)

time.sleep(1)

resp1 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['openapi-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {'CidrIp': cidr_dict['candy-crawler']},
                {'CidrIp': cidr_dict['candy-crawler-orderbook']},
                {'CidrIp': cidr_dict['candy-crawler-price']},
                {'CidrIp': cidr_dict['candy-db-redis']},
                {'CidrIp': cidr_dict['candy-deploy']},
                {'CidrIp': cidr_dict['candy-halls']},
                {'CidrIp': cidr_dict['candy-halls-cow']},
                {'CidrIp': cidr_dict['candy-ricola']},
                {'CidrIp': cidr_dict['office']},
                {'CidrIp': cidr_dict['pecunian-tokyo']}
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {'CidrIp': cidr_dict['candy-crawler']},
                {'CidrIp': cidr_dict['candy-crawler-orderbook']},
                {'CidrIp': cidr_dict['candy-crawler-price']},
                {'CidrIp': cidr_dict['candy-db-redis']},
                {'CidrIp': cidr_dict['candy-deploy']},
                {'CidrIp': cidr_dict['candy-halls']},
                {'CidrIp': cidr_dict['candy-halls-cow']},
                {'CidrIp': cidr_dict['candy-ricola']},
                {'CidrIp': cidr_dict['office']},
                {'CidrIp': cidr_dict['pecunian-tokyo']}
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)


print("### Results of revoking ingress SG of openapi LB ###")
print(resp1)

time.sleep(1)

resp2 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['openapi'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['openapi-lb'],
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    # DryRun = True
)

print("### Results of revoking ingress SG to openAPI server ###")
print(resp2)

time.sleep(5)

resp3 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['openapi'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['openapi-lb'],
                    'Description': 'http via LB',
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    # DryRun = True
)

print("### Results of authorizing ingress SG to openAPI server ###")
print(resp3)

