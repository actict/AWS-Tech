#!/usr/bin/env python3
# create_IOPS_alarms_eth-svr-phnx.py
#
# Last Updated: 2018.11.16
# Updated by: scott.hwang@peertec.com
#
# This script creates cloudwatch alarms for an io1 IO-optimized
# disk storing the Ethereum blockchain. This disk has a capacity
# of 1000GB (1TB) and has 4000 IOPS reserved.


import boto3


volid = 'vol-050918461e8d68fba'
sns_topic_wallet = 'arn:aws:sns:ap-northeast-2:762015387773:wallet-svr_cloudwatch_logs'

session = boto3.Session(profile_name = 'prod')
cwatchClient = session.client('cloudwatch')
readIOPS_max = 3000
readops_max = readIOPS_max * 60
writeIOPS_max = 1000
writeops_max = writeIOPS_max * 60

print("Creating eth-svr-phnx read IOPS alarm")
resp = cwatchClient.put_metric_alarm(
    AlarmName = 'eth-svr-phnx-read-IOPS-gt-3000',
    AlarmDescription = 'Alarm when Read I/O Ops gt 180,000 in 1 min',
    ComparisonOperator = 'GreaterThanThreshold',
    EvaluationPeriods = 5,
    MetricName = 'VolumeReadOps',
    Namespace = 'AWS/EBS',
    Period = 60,
    Statistic = 'Average',
    Threshold = readops_max,
    AlarmActions = [
        sns_topic_wallet
    ],
    Dimensions = [
        {
          'Name': 'VolumeId',
          'Value': volid
        },
    ],
    Unit = 'Count')

if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("Alarm creation SUCCESS")
else:
    print("Alarm creation ERROR")
    print(resp)

print("Creating eth-svr-phnx write IOPS alarm")
resp = cwatchClient.put_metric_alarm(
    AlarmName = 'eth-svr-phnx-write-IOPS-gt-1000',
    AlarmDescription = 'Alarm when Write I/O Ops gt 60,000 in 1 min',
    ComparisonOperator = 'GreaterThanThreshold',
    EvaluationPeriods = 5,
    MetricName = 'VolumeReadOps',
    Namespace = 'AWS/EBS',
    Period = 60,
    Statistic = 'Average',
    Threshold = writeops_max,
    AlarmActions = [
        sns_topic_wallet
    ],
    Dimensions = [
        {
          'Name': 'VolumeId',
          'Value': volid
        },
    ],
    Unit = 'Count')

if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("Alarm creation SUCCESS")
else:
    print("Alarm creation ERROR")
    print(resp)
