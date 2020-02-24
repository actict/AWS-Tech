#!/usr/bin/env python3
# create_sns_topics_service-admin.py
#
# Last Updated: 2019.07.09
# Updated by: scott.hwang@peertec.com, scott.hwang@actwo.com
#
# This boto3 script will create multiple new AWS Simple Notification
# Service (SNS) topics for AWS PROD service-admin-prod server and then add an
# email subscription for Slack '장애대응', 'emergency@actwo.com', and
# a webhook subscription for Pagerduty


import boto3
import time


session = boto3.Session(profile_name = 'prod_sns_full')
snsClient = session.client('sns')

email1 = 'g8k2s3x6k3k9f9m6@whalex.slack.com'
email2 = 'emergency@actwo.com'
webhook='https://events.pagerduty.com/integration/daa1e3ba3e5b4a35a4de43d49b149765/enqueue'

# index 0: sns topic name
# index 1: sns display name
mydict = {
    'service-admin' : ['service-admin', 'svc-adm']
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

    print("### Adding emergency email endpoint to SNS Topic ... ###")
    resp = snsClient.subscribe(
        TopicArn = myTopArn,
        Protocol = 'email',
        Endpoint = email2
        )
    print(resp)

    print("### Adding Pagerduty https endpoint to SNS Topic ... ###")
    resp = snsClient.subscribe(
        TopicArn = myTopArn,
        Protocol = 'https',
        Endpoint = webhook
        )
    print(resp)
    print("My SNS Topic ARN is %s" %myTopArn)

    time.sleep(1)
