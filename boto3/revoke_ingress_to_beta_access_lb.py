#!/usr/bin/env python3

# revoke_ingress_to_beta_access_lb.py
#
# Created on Apr 24, 2019 by joshua.huh@actwo.com
# Last Updated: 2019.10.21
# Updated by: scott.hwang@peertec.com, joshua.huh@actwo.com
#
# Purpose: revoke ALL ingress traffic to beta-access LB for
# Elastic Beanstalk app environment 'beta-access' and set
# LB idle timeout to 1s to cut off connections in flight.


import boto3
from env_prod import sec_group_dict, cidr_dict
from env_prod import load_balancer_dict
import time


session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')
elb2Client = session.client('elbv2')

resp1 = elb2Client.modify_load_balancer_attributes(
    LoadBalancerArn = load_balancer_dict['access-beta']['lb-arn'],
    Attributes = [
        {
            'Key' : 'idle_timeout.timeout_seconds',
            'Value' : '1'
        },
    ]
)

time.sleep(1)

resp = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['access-beta-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                { 'CidrIp': cidr_dict['nat-gw-2a']},
                { 'CidrIp': cidr_dict['nat-gw-2c']},
                { 'CidrIp': cidr_dict['nat-gw-dmz']},
                { 'CidrIp': cidr_dict['office']},
                { 'CidrIp': cidr_dict['vpc-gdac']}
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                { 'CidrIp': cidr_dict['nat-gw-2a']},
                { 'CidrIp': cidr_dict['nat-gw-2c']},
                { 'CidrIp': cidr_dict['nat-gw-dmz']},
                { 'CidrIp': cidr_dict['office']},
                { 'CidrIp': cidr_dict['vpc-gdac']}
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)

print("### Results of changing beta-access LB idle timeout to 1 sec ###")
print(resp1)

print("### Results of revoking beta-access LB SG ingress ###")
print(resp)
