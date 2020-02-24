#!/usr/bin/env python3
# ebs_snapshots_ec2_dec_2018.py
#
# Last Updated: 2018.12.12
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to take snapshots of root disks from
# various EC2 instances before maintenance tasks will be
# executed. After taking snapshots, the script will keep checking
# the snapshot state until they all return 'State': 'completed'


import boto3
from env_prod import *
import time


session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')
volumeIdList = [
    vol_internal_api_root,
    vol_match_root,
    vol_beta_front_root,
    vol_admin_access_root,
    vol_admin_front_root,
    vol_cruizer_root,
    vol_ledger_root,
    vol_kakaopay_root
    ]
snapIdList = list()

for vol in volumeIdList:
    print("Taking snapshot of vol: %s" % vol)
    resp = ec2Client.create_snapshot(
        VolumeId = vol
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
