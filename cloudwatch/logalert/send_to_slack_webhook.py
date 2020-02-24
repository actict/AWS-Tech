#!/usr/bin/env python3
# send_to_slack_webhook.py
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This toy script shows an example of sending a simple text message
# to a slack channel via its webhook endpoint.


import json
import requests


# The following webhook is for #notify_fds Slack channel
webhook_url = 'https://hooks.slack.com/services/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'

payload = {"text":
           "This is text line 1.\n"
           "This is text line 2."
           }

print("Sending text to slack channel %s ..." %webhook_url)
resp = requests.post(
    webhook_url,
    json.dumps(payload),
    headers = {'Content-Type': 'application/json'}
)

print(resp)
