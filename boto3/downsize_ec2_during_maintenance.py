#!/usr/bin/env python3
# downsize_ec2_during_maintenance.py
#
# Last Updated: 2018.11.27
# Updated by: scott.hwang@peertec.com
#
# This script uses ec2client methods stop_instances() and
# modify_instance_attribute() and start_instances() from boto3 to
# change EC2 instance type to a smaller one and then start the
# instance


import boto3
import time
from env_prod import *


dictOfInst = {
    'wallet' : [sns_wallet, iid_wallet_svr, 'm5.large'],
    'match0' : [sns_match0, iid_match0_svr, 'c5.large'],
    'ops-connector' : ['', iid_ops_connect, 't2.medium']
    }

session = boto3.Session(profile_name = 'prod')
ec2Client = session.client('ec2')

for mykey in dictOfInst:
    print("### Stopping instance %s ###" % mykey)
    resp_stop = ec2Client.stop_instances(
        InstanceIds = [dictOfInst[mykey][1]])

    if resp_stop['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("### Instance %s stop SUCCESS ###" % mykey)
    else:
        print("Stopping instance %s FAILED!")

print("Waiting for instances to fully stop...")
time.sleep(60)

for mykey in dictOfInst:
    print("### Modifying instance %s ###" % mykey)
    resp_modify = ec2Client.modify_instance_attribute(
        InstanceId = dictOfInst[mykey][1],
        InstanceType = {
            'Value': dictOfInst[mykey][2]
        }
    )

    if resp_modify['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("### Instance %s modify SUCCESS ###" % mykey)
    else:
        print("Modifying instance %s FAILED!")

print("Waiting for instance modify to complete...")
time.sleep(20)

for mykey in dictOfInst:
    print("### Starting instance %s ###" % mykey)
    resp_start = ec2Client.start_instances(
        InstanceIds = [dictOfInst[mykey][1]])

    if resp_start['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("### Instance %s start SUCCESS ###" % mykey)
    else:
        print("Starting instance %s FAILED!")
