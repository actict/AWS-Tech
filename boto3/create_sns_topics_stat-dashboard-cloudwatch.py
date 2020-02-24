#!/usr/bin/env python3
#Create_sns_topics_stat-dashboard-cloudwatch.py
#
# Last Updated: 2019.09.16
# Updated by: scott.hwang@peertec.com, scott.hwang@actwo.com
#
# This boto3 script will create multiple new AWS Simple Notification
# Service (SNS) topics for AWS PROD stat-dashboard server and then add an
# email subscription for Slack '장애대응'


import boto3
import time


session = boto3.Session(profile_name = 'prod_sns_full')
snsClient = session.client('sns')

email1 = 'v8w4z2a9o5a3g7f9@peertec.slack.com'

# index 0: sns topic name
# index 1: sns display name
mydict = {
    'stat-dashboard' : ['stat-dashboard-cloudwatch', 'stdashlog']
    }


for k in mydict:
    print("### Creating SNS Topic for %s ###" %k)
    resp = snsClient.create_topic(
        Name = mydict[k][0])
    myTopArn = resp['TopicArn']

    print("### Editing SNS Topic Display Settings... ###")
    resp = snsClient.set_topic_attributes(
        TopicArn = myTopArn,
        AttributeName = 'DisplayName',
        AttributeValue = mydict[k][1]
        )
    print(resp)

    print("### Adding Slack 장애대응 mail endpoint to SNS Topic ... ###")
    resp = snsClient.subscribe(
        TopicArn = myTopArn,
        Protocol = 'email',
        Endpoint = email1
        )
    print(resp)

    print("My SNS Topic ARN is %s" %myTopArn)

    time.sleep(1)
