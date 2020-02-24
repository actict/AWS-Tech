#!/usr/bin/env python3
# ebs_snapshots_ec2_mar_2019.py
#
# Last Updated: 2019.03.19
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to take snapshots of root disks from
# various EC2 instances before maintenance tasks will be
# executed. After taking snapshots, the script will keep checking
# the snapshot state until they all return 'State': 'completed'
# NOTE: it is not necessary to wait until all snapshots return
# 'completed' to know if a snapshot is successful or not; EBS
# snapshots are made at a point-in-time, so you can continue using
# the underlying disk even after having started an EBS snap.
#
# This script version adds tags to EBS snapshots. This feature was
# added in April 2018 and is supported in recent Boto3 releases.
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_snapshot



import boto3
from env_prod import *
import time


session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')
volumeIdList = [
    vol_admin_tonghap_root,
    vol_auth_bank_root,
    vol_bip_blockinpress_root,
    vol_bip_deconomy_root,
    vol_bip_mysql_root,
    vol_bitgo_api_root,
    vol_bitgo_webhook_root,
    vol_cruizer_root,
    vol_etc_prod_root,
    vol_geth1_root,
    vol_geth2_root,
    vol_geth_ng_root,
    vol_hdac_root,
    vol_gl_batch_0,
    vol_gl_batch_1,
    vol_gl_batch_2,
    vol_internal_api_root,
    vol_jenkins_root,
    vol_kakaopay_root,
    vol_ledger_root,
    vol_ledger_sdb,
    vol_logstash_root,
    vol_match_root,
    vol_pd_root,
    vol_prod_front_1,
    vol_prod_front_2,
    vol_prod_front_3,
    vol_prod_front_4,
    vol_prod_front_alpha,
    vol_prod_front_beta,
    vol_svc_admin_root,
    vol_wallet_root
    ]
snapIdList = list()

for vol in volumeIdList:
    print("Taking snapshot of vol: %s" % vol)
    resp = ec2Client.create_snapshot(
        VolumeId = vol,
        TagSpecifications = [
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'note',
                        'Value': '2019.03.20 maintenance'
                    },
                ]
            },
        ],
    DryRun = False
    )
    snapIdList.append(resp['SnapshotId'])

resp1 = ec2Client.describe_snapshots(
    SnapshotIds = snapIdList
    )

readyCnt = 0  # counter for 'complete' snapshots
while readyCnt < len(snapIdList):
    readyCnt = 0  # reinitialize at start of while loop
    print("Checking if all snapshots are complete...")
    for i in range(len(resp1['Snapshots'])):
        if resp1['Snapshots'][i]['State'] == 'completed':
            readyCnt += 1
    print("%d of %d snapshots are complete" %(readyCnt, len(snapIdList)))
    time.sleep(10)

print("All snapshots are complete")
