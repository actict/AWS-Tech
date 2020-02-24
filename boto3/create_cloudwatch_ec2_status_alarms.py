#!/usr/bin/env python3
# create_cloudwatch_ec2_status_alarms.py
#
# Last Updated: 2018.11.27
# Updated by: scott.hwang@peertec.com
#
# This script will create cloudwatch EC2 status alarms that will
# send notifications to an AWS SNS topic for a given EC2 instance.


import boto3
from env_prod import *


dictOfInst = {
    'prod-front-1' : [sns_prod_front_1, iid_prod_front_1],
    'prod-front-2' : [sns_prod_front_2, iid_prod_front_2],
    'ledger' : [sns_ledger, iid_ledger],
    'etc-prod' : [sns_etc_classic, iid_etc_classic],
    'eth-twin' : [sns_eth_twin, iid_eth_twin],
    'bitgo-webhook' : [sns_bitgo_webhook, iid_bitgo_webhook],
    'bitgo-api' : [sns_bitgo_api, iid_bitgo_api],
    'wireguard' : [sns_wireguard, iid_vpn_wireguard],
    'ssl-cert-mgmt' : [sns_ssl_cert, iid_ssl_cert_mgmt],
    'cruizer' : [sns_cruizer, iid_cruizer],
    'maintenance' : [sns_maint, iid_fr_maintenance],
    'auth-kakaopay' : [sns_kakaopay, iid_auth_kakaopay]
    }

session = boto3.Session(profile_name = 'prod')
cwatchClient = session.client('cloudwatch')

for mykey in dictOfInst:
    print("Creating status alarm for server %s" % mykey)
    respP = cwatchClient.put_metric_alarm(
        AlarmName = mykey + '-status-check-failed',
        AlarmDescription = 'Alarm if AWS EC2 status check fails 2 times in 2 min',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 2,
        MetricName = 'StatusCheckFailed',
        Namespace = 'AWS/EC2',
        Period = 60,
        Statistic = 'Average',
        Threshold = 2,
        AlarmActions = [dictOfInst[mykey][0]],
        Dimensions = [
            {
                'Name': 'InstanceId',
                'Value': dictOfInst[mykey][1]
            },
        ],
        Unit = 'Count')

    if respP['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("%s status alarm creation SUCCESS" % mykey)
    else:
        print("%s status alarm creation ERROR" % mykey)
        print(respP)
