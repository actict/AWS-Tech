#!/usr/bin/env python3

# authorize_ingress_to_beta_access_lb.py
#
# Created on Apr 24, 2019 by joshua.huh@actwo.com
# Last Updated: 2019.10.21
# Updated by: jun.go@peertec.com, joshua.huh@actwo.com
#
# Purpose: allow ingress traffic to beta-access


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
            'Value' : '60'
        },
    ]
)

time.sleep(1)

resp2 = ec2Client.authorize_security_group_ingress(
    GroupId = sec_group_dict['access-beta-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'IpRanges': [
                { 'CidrIp': cidr_dict['nat-gw-2a'],
                  'Description': 'acc via nat gw 1'},
                { 'CidrIp': cidr_dict['nat-gw-2c'],
                  'Description': 'acc via nat gw 2'},
                { 'CidrIp': cidr_dict['nat-gw-dmz'],
                  'Description' : 'acc via nat gw 3'},
                { 'CidrIp': cidr_dict['office'],
                  'Description' : 'acc from office'},
                { 'CidrIp': cidr_dict['vpc-gdac'],
                  'Description' : 'CHECK. IS THIS NECESSARY'}
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                { 'CidrIp': cidr_dict['nat-gw-2a'],
                  'Description': 'acc via nat gw 1'},
                { 'CidrIp': cidr_dict['nat-gw-2c'],
                  'Description': 'acc via nat gw 2'},
                { 'CidrIp': cidr_dict['nat-gw-dmz'],
                  'Description' : 'acc via nat gw 3'},
                { 'CidrIp': cidr_dict['office'],
                  'Description' : 'acc from office'},
                { 'CidrIp': cidr_dict['vpc-gdac'],
                  'Description' : 'CHECK. IS THIS NECESSARY'}
            ],
            'ToPort': 443
        }
    ],
    # DryRun = True
)

print("### Results of changing beta-access LB idle timeout to 60 sec ###")
print(resp1)

print("### Results of opening all ingress to beta-access LB ###")
print(resp2)
