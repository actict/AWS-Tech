#!/usr/bin/env python3
# ebs_snapshots_ec2_nov_2018.py
#
# Last Updated: 2018.12.12
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to take snapshots of root disks from
# various EC2 instances before maintenance tasks will be
# executed. After taking snapshots, the script will keep checking
# the snapshot state until they all return 'State': 'completed'


import boto3
import time


session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')
volumeIdList = [
    'vol-06770df0f8da93bf0',
    'vol-08ebce2a43cbb25ad',
    'vol-007b63983203af787',
    'vol-00b1293006c8b613c',
    'vol-03822a1e645c40044',
    'vol-0f17b0329ab6ce584',
    'vol-0a203d9ef54e31b47',
    'vol-0698ef2d86ffdb09f',
    'vol-0ae70a35520fa9cdc',
    'vol-06c793eea886bbb88',
    'vol-04bc2d9cedcfef1b6',
    'vol-03f0520764995c506',
    'vol-0073671c9c797a225',
    'vol-0bcfecc746abeee7f',
    'vol-0260453bc95660bae'
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
