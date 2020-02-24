#!/usr/bin/env python3

'''
revoke_ingress_to_gmartapi_lb

Last Updated: 2019.10.21
Created by: joshua.huh@actwo.com
Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com
Purpose: revoke ALL ingress traffic to gmart api LB and set the LB
idle timeout to 1s to cut off connections in-flight.

Revoking ingress traffic in LB is NOT enough!!!
Even minimum idle timeout is too log to clear all sessions.
Temporary traffic choking in the server is required.
'''


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['gmart-api']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '1'
        },
    ]
)

print("### Results of changing marketapi LB idle timeout to 1 sec ###")
print(resp)

time.sleep(1)

resp1 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['gmart-api-lb'],
    IpPermissions = [
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [{'CidrIp': cidr_dict['any-ip']}],
            'ToPort': 443
        },
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [{'CidrIp': cidr_dict['any-ip']}],
            'ToPort': 80
        }
    ],
    # DryRun = True
)

print("### Results of revoking ingress SG of marketapi LB ###")
print(resp1)

resp2 = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['gmart-api'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['gmart-api-lb'],
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    # DryRun = True
)

print("### Results of revoking ingress SG to gmart-api server ###")
print(resp2)

time.sleep(5)

resp3 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['gmart-api'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    'GroupId': sec_group_dict['gmart-api-lb'],
                    'Description': 'http via LB',
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        }
    ],

    # DryRun = True
)

print("### Results of authorizing ingress SG to gmart-api server ###")
print(resp3)
