#!/usr/bin/env python3
# create_IOPS_alarms_etc-mainnet.py
#
# Last Updated: 2018.11.19
# Updated by: hulk.choi@actwo.com, scott.hwang@peertec.com
#
# This script creates cloudwatch alarms for an io1 IO-optimized
# disk storing the Ethereum blockchain. This disk has a capacity
# of 1000GB (1TB) and has 3000 IOPS reserved.


import boto3


volid = 'vol-09f084374a19990d0'
sns_topic_wallet = 'arn:aws:sns:ap-northeast-2:905136931838:walletNoti'

session = boto3.Session(profile_name = 'dev')
cwatchClient = session.client('cloudwatch')
readIOPS_max = 2330
readops_max = readIOPS_max * 60
writeIOPS_max = 670
writeops_max = writeIOPS_max * 60

print("Creating etc-mainnet read IOPS alarm")
resp = cwatchClient.put_metric_alarm(
    AlarmName = 'etc-mainnet-read-IOPS-gt-2330',
    AlarmDescription = 'Alarm when Read I/O Ops gt 139,800 in 1 min',
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

print("Creating etc-mainnet write IOPS alarm")
resp = cwatchClient.put_metric_alarm(
    AlarmName = 'etc-mainnet-write-IOPS-gt-670',
    AlarmDescription = 'Alarm when Write I/O Ops gt 40,200 in 1 min',
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
