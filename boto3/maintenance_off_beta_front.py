#!/usr/bin/env python3

'''
maintenance_off_beta_front.py

Created: 2019.4.24 by joshua.huh@actwo.com
Updated: 2019.10.21
Updated by: jun.go@peertec.com

Purpose: allow ssh and http(s) to beta front
'''

import boto3
from env_prod import instance_id_dict, sec_group_dict

session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')

resp = ec2Client.modify_instance_attribute(
    InstanceId = instance_id_dict['fr-beta'],
    Groups = [
        sec_group_dict['wireguard-http'],
        sec_group_dict['wireguard-https'],
        sec_group_dict['wireguard-ssh']
    ],
    # DryRun = True
)
print(resp)
