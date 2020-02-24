#!/usr/bin/env python3
# create_sns_topic_terra_full.py
#
# Last Updated: 2019.05.28
# Updated by: scott.hwang@actwo.com
#
# This boto3 script will create a new AWS Simple Notification Service
# (SNS) topic and then add an email subscription for Slack '장애대응',
# 'emergency@actwo.com', and a webhook subscription for Pagerduty


import boto3


session = boto3.Session(profile_name = 'prod_sns_full')
snsClient = session.client('sns')

print("### Creating SNS Topic... ###")
resp = snsClient.create_topic(
    Name = 'terra-full')
myTopArn = resp['TopicArn']

print("### Editing SNS Topic Display Settings... ###")
resp = snsClient.set_topic_attributes(
    TopicArn = myTopArn,
    AttributeName = 'DisplayName',
    AttributeValue = 'terraFull'
    )
print(resp)

print("### Adding Slack 장애대응 mail endpoint to SNS Topic ... ###")
resp = snsClient.subscribe(
    TopicArn = myTopArn,
    Protocol = 'email',
    Endpoint = 'g8k2s3x6k3k9f9m6@whalex.slack.com'
    )
print(resp)


print("### Adding emergency email endpoint to SNS Topic ... ###")
resp = snsClient.subscribe(
    TopicArn = myTopArn,
    Protocol = 'email',
    Endpoint = 'emergency@actwo.com'
    )
print(resp)

print("### Adding Pagerduty https endpoint to SNS Topic ... ###")
resp = snsClient.subscribe(
    TopicArn = myTopArn,
    Protocol = 'https',
    Endpoint = 'https://events.pagerduty.com/integration/daa1e3ba3e5b4a35a4de43d49b149765/enqueue'
    )
print(resp)
print("My SNS Topic ARN is %s" %myTopArn)
