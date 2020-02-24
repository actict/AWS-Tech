#!/usr/bin/env python3

# authorize_ingress_to_access_lb.py
#
# Last Updated: 2019.10.21
# Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com
#
# Purpose: allow ALL ingress traffic to ALB for Elastic Beanstalk
# app environment 'prod-access' and set LB idle timeout to 60s
# default


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp1 = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['access']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '60'
        },
    ]
)

time.sleep(1)

resp = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['access-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': cidr_dict['any-ip'],
                    'Description': 'access to api.gdac.com'
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
                    'Description': 'access to api.gdac.com'
                }
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)

print("### Results of changing prod-access LB idle timeout to 60 sec ###")
print(resp1)

print("### Results of opening SG ingress for prod-access lb ###")
print(resp)

