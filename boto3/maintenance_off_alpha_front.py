#!/usr/bin/env python3

'''
maintenance_off_alpha_front.py

Created: 2019.4.24 by joshua.huh@actwo.com
Updated: 2019.10.21
Updated by: jun.go@peertec.com

Purpose: allow ssh and web session to alpha front

Note: I'm not sure why Joshua made `maintenance_on*.py` and
`maintenance_off*.py` because both scripts simply add security
groups to instances... perhaps he is adding different kinds of
security groups?
'''

import boto3
from env_prod import instance_id_dict, sec_group_dict

session = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client = session.client('ec2')

resp = ec2Client.modify_instance_attribute(
    InstanceId = instance_id_dict['fr-alpha'],
    Groups = [
        sec_group_dict['wireguard-http'],
        sec_group_dict['wireguard-https'],
        sec_group_dict['wireguard-ssh']
    ],
    # DryRun = True
)
print(resp)
