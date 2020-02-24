#!/usr/bin/env python3

'''
revoke_ingress_to_general_vpn_lb.py

Created on May 14, 2019 by joshua.huh@actwo.com
Updated on: 2019.10.21
Updated by: jun.go@peertec.com

Purpose: deny ingress traffic to openapi via VPN
'''

import boto3
from env_prod import sec_group_dict, cidr_dict

session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')

resp = ec2Client.revoke_security_group_ingress(
    GroupId = sec_group_dict['vpn-lb'],
    IpPermissions = [
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    # SHOULD be 'wireguard', no 'wireguard-http' here.
                    # 'wireguard-http' in EC2, 'wireguard' in Beanstalk.
                    'GroupId': sec_group_dict['wireguard'],
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 80
        },
        {
            'FromPort': 443,
            'IpProtocol': 'tcp',
            'UserIdGroupPairs': [
                {
                    # SHOULD be 'wireguard', no 'wireguard-https' here.
                    # 'wireguard-http' in EC2, 'wireguard' in Beanstalk.
                    'GroupId': sec_group_dict['wireguard'],
                    'UserId': '762015387773'
                }
            ],
            'ToPort': 443
        }
    ],

    #DryRun = True
)
print(resp)
