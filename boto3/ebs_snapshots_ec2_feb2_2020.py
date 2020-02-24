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
    'terrafull-root',
    'terralcd-root',
    'wallet-root',
    'cmt-root',
    'cosmos-lcd-root',
    'etc-root',
    'geth1-root',
    'geth2-root',
    'hdac-root',
    'irisnet-full-root',
    'irisnet-lcd-root',
    'pay-orderbot-root',
    'hashtower-root',
    'blockinpress-mysql',
    'peertecweb-root',
    'blockinpress-root',
    'deconomy-root',
    'front1-root',
    'front2-root',
    'ledger-root',
    'match-root',
    'auth-bank-root',
    'kakaopay-root',
    'bitgo-api-root',
    'bitgo-webhook-clone-root',
    'tx-verifier-root'
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
                            'Value': '2020.02.05 maintenance'
                        },
                    ]
                },
            ],
        DryRun = False
        )
        snapIdList_prod.append(resp['SnapshotId'])

print("All snapshots are complete")
