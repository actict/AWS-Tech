#!/usr/bin/env python3
# ebs_snapshots_ec2_oct_2019.py
#
# Last Updated: 2019.10.22
# Updated by: scott.hwang@peertec.com,scott.hwang@actwo.com
#
# This script uses boto3 to take snapshots of root disks from
# various EC2 instances before maintenance tasks will be
# executed. After taking snapshots, the script will keep checking
# the snapshot state until they all return 'State': 'completed'.
#
# NOTE: It is NOT necessary to wait until all snapshots return
# 'completed' to know if a snapshot is successful or not; EBS
# snapshots are made at a point-in-time, so you can continue using
# the underlying disk even after having started an EBS snap.
#
# This is the first version of the EBS snapshot script to include
# root disk volumes from AWS Pecunian account.


import boto3
from env_prod import ebs_vol_dict as vol_dict_prod

session0 = boto3.Session(profile_name = 'prod_ec2_full')
ec2Client0 = session0.client('ec2')

snap_vols_prodL = [
    'admin-root',
    'auth-bank-root',
    'bitgo-api-root',
    'bitgo-webhook-root',
    'blockinpress-mysql',
    'blockinpress-root',
    'certmanager-root'
    'cmt-root',
    'cosmos-lcd-root',
    'cruiser-root',
    'deconomy-root',
    'etc-root',
    'front1-root',
    'front2-root',
    'front-alpha-root',
    'front-beta-root',
    'fx-root',
    'geth1-root',
    'geth2-root',
    'gl-batch0-root',
    'gl-batch1-root',
    'gl-batch2-root',
    'grow-blockeye-root',
    'grow-dealer-root',
    'grow-reward-root',
    'grow-vault-root',
    'hashivault-root',
    'hashtower-root',
    'hdac-root',
    'internal-api-root',
    'irisnet-full-root',
    'irisnet-lcd-root',
    'jenkins-root',
    'kakaopay-root',
    'ledger-root',
    'logger-root',
    'maintenance-root',
    'match-root',
    'pay-orderbot-root',
    'peertec-prod-root',
    'pl-batch0-root',
    'service-admin-root',
    'statdashb-root',
    'terrafull-root',
    'terralcd-root',
    'wallet-root'
]

snapIdList_prod = list()

for vol in vol_dict_prod:
    if vol in snap_vols_prodL:
        print("Taking snapshot of : %s disk" % vol)
        resp = ec2Client0.create_snapshot(
            VolumeId = vol_dict_prod[vol],
            TagSpecifications = [
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'note',
                            'Value': '2019.10.22 maintenance'
                        },
                    ]
                },
            ],
        DryRun = False
        )
        snapIdList_prod.append(resp['SnapshotId'])

print("All snapshots are complete")
