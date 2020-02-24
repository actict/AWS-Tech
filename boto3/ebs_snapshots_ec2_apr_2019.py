#!/usr/bin/env python3
# ebs_snapshots_ec2_apr_2019.py
#
# Last Updated: 2019.05.14
# Updated by: scott.hwang@peertec.com
#
# This script uses boto3 to take snapshots of root disks from
# various EC2 instances before maintenance tasks will be
# executed. After taking snapshots, the script will keep checking
# the snapshot state until they all return 'State': 'completed'
#
# NOTE: It is not necessary to wait until all snapshots return
# 'completed' to know if a snapshot is successful or not; EBS
# snapshots are made at a point-in-time, so you can continue using
# the underlying disk even after having started an EBS snap.
#
# This script version adds tags to EBS snapshots. This feature was
# added in April 2018 and is supported in recent Boto3 releases.
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_snapshot



import boto3
from env_prod import ebs_vol_dict
import time


session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')

snap_volsL = [
    'admin-root',
    'auth-bank-root',
    'bitgo-api-root',
    'bitgo-webhook-root',
    'blockinpress-mysql',
    'blockinpress-root',
    'cmt-root',
    'cruiser',
    'deconomy-root',
    'etc-root',
    'front-1',
    'front-2',
    'front-3',
    'front-4',
    'front-alpha-root',
    'front-beta-root',
    'geth1-root',
    'geth2-root',
    'geth-ng-root',
    'gl-batch0-root',
    'gl-batch1-root',
    'gl-batch2-root',
    'hashivault-root',
    'hdac-root',
    'internal-api-root',
    'irisnet-full-root',
    'jenkins-root',
    'kakaopay-root',
    'ledger-root',
    'logger-root',
    'match-root',
    'pd-root',
    'service-admin',
    'wallet-root'
]

snapIdList = list()

for vol in ebs_vol_dict:
    if vol in snap_volsL:
        print("Taking snapshot of : %s disk" % vol)
        resp = ec2Client.create_snapshot(
            VolumeId = ebs_vol_dict[vol],
            TagSpecifications = [
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'note',
                            'Value': '2019.05.14 maintenance'
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
