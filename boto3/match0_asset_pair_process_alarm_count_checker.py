#!/usr/bin/env python3
# match0_asset_pair_process_alarms_count_checker.py
#
# Last Updated: 2019.02.27
# Updated by: scott.hwang@peertec.com
#
# This script counts the number of asset pair matching
# processes with a certain naming pattern and compares this
# value with the number of *active* asset pairs in PROD AuroraDB
# table 'whalex.TC_TRADE_PAIR'. If these two counts do not match,
# an alert will be sent to Slack channel #notify_match stating
# whether there are too many or too few process alarms. (Then
# someone from the infra team will have to delete or add
# cloudwatch alarms so that the two counts converge)


import argparse
import boto3
import json
import pymysql
import requests
import time
from mysqlSecrets import prod_db_ro
from mysqlSecrets import prod_user
from mysqlSecrets import prod_user_pw


def send_to_slack(endpoint, data):
    """
    str, str -> HTTP POST

    Given an http(s) endpoint and string data, send the data as
    a JSON payload to a Slack webhook.
    """
    payload = {
        "username": "!match0 process alarm counter",
        "text": data
    }
    print("Sending text to slack channel %s ..." % endpoint)
    resp = requests.post(
        endpoint,
        json.dumps(payload),
        headers = {'Content-Type': 'application/json'}
    )
    return resp


def slack_send_status_ck(reqObj):
    """
    requests Object -> str on stdout

    Given a python 'requests' object, check the response status code
    (HTTP status code) and print a message to stdout depending on the
    result of 'reqObj.status_code'
    """
    if reqObj.status_code != 200:
        print("**Sending payload to Slack webhook FAILED**")
    else:
        print("Sending payload to Slack webhook SUCCEEDED")


def cw_proc_alarm_counter(cwSessObj, alNamePattern):
    """
    boto3CloudwatchSessionObj, str -> int

    Given a boto3 Cloudwatch Session Object and a process alarm
    name pattern as str, return an integer denoting the number
    of alarms matching the pattern in 'alNamePattern'
    """
    resp = cwSessObj.describe_alarms(
        AlarmNamePrefix = alNamePattern
        )

    return len(resp['MetricAlarms'])


def get_active_tc_trade_pair(dbcursorObj):
    """
    pymysql cursor Obj -> int

    Given a pymysql cursor object created from a 'whalex' db
    connection, get the row count of active asset pairs from
    the table TC_TRADE_PAIR.
    """
    query_active = "SELECT COUNT(*) FROM TC_TRADE_PAIR WHERE state='A';"
    dbcursorObj.execute(query_active)
    resp = dbcursorObj.fetchall()
    active_count = resp[0]['COUNT(*)']
    return active_count


def main():
    start = time.time()
    # argparse boilerplate
    parser = argparse.ArgumentParser(
        description="Given an AWS envo profile_name, count the "
        "number of Cloudwatch collectd process alarms on 'match0' "
        "and compare this number to the number of Active pairs in "
        "whalex.TC_TRADE_PAIR.")
    parser.add_argument('awsenvo', type = str, help = "name of aws "
                        "'profile_name' defined in ~/.aws/...")
    args = parser.parse_args()

    session = boto3.Session(profile_name = args.awsenvo)
    cwClient = session.client('cloudwatch')
    db_session = pymysql.connect(prod_db_ro, prod_user, prod_user_pw,
                                 database='whalex')
    db_cursor = db_session.cursor(pymysql.cursors.DictCursor)
    slack_webhook_match0 = 'https://hooks.slack.com/services/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'

    match_proc_count = cw_proc_alarm_counter(cwClient, 'match0-match_')
    trade_proc_count = cw_proc_alarm_counter(cwClient, 'match0-trade_')
    tc_trade_pair_active_cnt = get_active_tc_trade_pair(db_cursor)

    print("There are %d process alarms for match_no_th*.py"
        % match_proc_count)
    print("There are %d process alarms for trade_receiver_v2*.py"
        % trade_proc_count)
    print("There are %d active pairs in TC_TRADE_PAIR"
        % tc_trade_pair_active_cnt)

    if match_proc_count < tc_trade_pair_active_cnt:
        msg = ("%d `match_no_th.py` process alarms is *less than* "
        "%d active pairs in `whalex.TC_TRADE_PAIR`! You may "
        "need to add some Cloudwatch Alarms for processes on `match0`."
        %(match_proc_count, tc_trade_pair_active_cnt))
        print(msg)
        slresp = send_to_slack(slack_webhook_match0, msg)
        slack_send_status_ck(slresp)
    elif match_proc_count > tc_trade_pair_active_cnt:
        msg = ("%d `match_no_th.py` process alarms is "
        "*greater than* %d active pairs in "
        "`whalex.TC_TRADE_PAIR`! You may need to remove some Cloudwatch "
        "Alarms for processes on `match0`."
        %(match_proc_count, tc_trade_pair_active_cnt))
        print(msg)
        slresp = send_to_slack(slack_webhook_match0, msg)
        slack_send_status_ck(slresp)

    if trade_proc_count < tc_trade_pair_active_cnt:
        msg = ("%d `trade_receiver_v2.py` process alarms is *less than* "
        "%d active pairs in `whalex.TC_TRADE_PAIR`! You may "
        "need to add some Cloudwatch Alarms for processes on `match0`."
        %(trade_proc_count, tc_trade_pair_active_cnt))
        print(msg)
        slresp = send_to_slack(slack_webhook_match0, msg)
        slack_send_status_ck(slresp)
    elif trade_proc_count > tc_trade_pair_active_cnt:
        msg = ("%d `trade_receiver_v2.py` process alarms is "
        "*greater than* %d active pairs in "
        "`whalex.TC_TRADE_PAIR`! You may need to remove some Cloudwatch "
        "Alarms for processes on `match0`."
        %(trade_proc_count, tc_trade_pair_active_cnt))
        print(msg)
        slresp = send_to_slack(slack_webhook_match0, msg)
        slack_send_status_ck(slresp)

    print("Closing DB session...")
    db_session.close()
    end = time.time()
    print("This script took %s seconds to run" % (end - start))

if __name__ == '__main__':
    main()
