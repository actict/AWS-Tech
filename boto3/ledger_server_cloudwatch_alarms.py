#!/usr/bin/env python3
# ledger_server_cloudwatch_alarms.py
#
# Last Updated: 2018.11.21
# Updated by: scott.hwang@peertec.com
#
# This script creates cloudwatch alarms for ledger server in
# PROD environment. These alarms include process alarms, status
# alarms, CPU, memory, disk alarms, etc.
#
# Note: for process alarms to work, first 'collectd.conf' must
# enable 'LoadPlugin processes' and process checks must be
# defined in a <Plugin processes></Plugin> block.
#
# Note that the name of the process monitor will be entered
# in the key-keyval pair {'Name':'PluginInstance', 'Value':'procmonName'}


import boto3


instId = 'i-024dd3062a1003ccd'
sns_topic_ledger = 'arn:aws:sns:ap-northeast-2:762015387773:ledger-tonghap-phoenix'

session = boto3.Session(profile_name = 'prod')
cwatchClient = session.client('cloudwatch')


print("Creating process alarm for ledger-admin index.js")
resp = cwatchClient.put_metric_alarm(
    AlarmName = 'ledger-admin-index.js-num-processes',
    AlarmDescription = 'Alarm when number of index.js processes lt 1 for 30sec',
    ComparisonOperator = 'LessThanThreshold',
    EvaluationPeriods = 3,
    MetricName = 'processes.ps_count.processes',
    Namespace = 'collectd',
    Period = 10,
    Statistic = 'Average',
    Threshold = 1,
    AlarmActions = [
        sns_topic_wallet
    ],
    Dimensions = [
        {
            'Name': 'Host',
            'Value': instId
        },
        {
            'Name': 'PluginInstance',
            'Value': 'admin'
        }
    ],
    Unit = 'Count')

if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("Alarm creation SUCCESS")
else:
    print("Alarm creation ERROR")
    print(resp)


print("Creating status alarm for ledger server")
resp1 = cwatchClient.put_metric_alarm(
    AlarmName = 'ledger-status-check-failed',
    AlarmDescription = 'Alarm if AWS status check fails twice in 2min',
    ComparisonOperator = 'GreaterThanOrEqualToThreshold',
    EvaluationPeriods = 2,
    DatapointsToAlarm = 2,
    MetricName = 'StatusCheckFailed',
    Namespace = 'AWS/EC2',
    Period = 60,
    Statistic = 'Average',
    Threshold = 1,
    AlarmActions = [
        sns_topic_wallet
    ],
    Dimensions = [
        {
            'Name': 'InstanceId',
            'Value': instId
        }
    ],
    Unit = 'Count')

if resp1['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("Alarm creation SUCCESS")
else:
    print("Alarm creation ERROR")
    print(resp1)
