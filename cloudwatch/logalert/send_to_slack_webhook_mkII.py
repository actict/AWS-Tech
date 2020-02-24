#!/usr/bin/env python3
# send_to_slack_webhook_mkII.py
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script sends a text payload read from a file to a slack
# channel's webhook endpoint.


import argparse
import json
import requests
import sys


parser = argparse.ArgumentParser(
    description="Send a text payload from a file to a Slack webhook. "
                "Arguments are 'filename' and 'webhook'")
parser.add_argument('filename', type = str, help = "file containing text "
                    "to send to Slack")
parser.add_argument('webhook', type = str, help = "http endpoint for Slack "
                    "channel")
parser.add_argument('username', type = str, help = "Displayed name in Slack")
args = parser.parse_args()

webhook_url = args.webhook

with open(args.filename, 'r') as f:
    results = f.read()

payload = {"username": args.username,
           "text": results}


print("Sending text to slack channel %s ..." %webhook_url)
resp = requests.post(
    webhook_url,
    json.dumps(payload),
    headers = {'Content-Type': 'application/json'}
)

if resp.status_code != 200:
    print("Sending payload to %s FAILED!" % args.webhook)
    sys.exit(1)
else:
    print("Sending payload to %s SUCCESS!" % args.webhook)
