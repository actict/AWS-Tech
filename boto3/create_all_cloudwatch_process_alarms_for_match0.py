#!/usr/bin/env python3
# create_all_cloudwatch_process_alarms_for_match0.py
#
# Last Updated: 2019.02.20
# Updated by: scott.hwang@peertec.com
#
# This script will create 30+ cloudwatch collectd process
# alarms for match0. These process alarms are mostly for
# asset pairs like BTC/KRW, GT/KRW, BOS/GT, etc. Each
# asset pair is managed by two python processes,
# 'match_no_th.py' and 'trade_receiver_v2.py'


import boto3
import time
from env_prod import iid_match0_svr
from env_prod import sns_match0
from lib_cloudwatch_alarms import create_collectd_process_alarm


def main():
    start = time.time()
    session = boto3.Session(profile_name = 'prod')
    cwClient = session.client('cloudwatch')

    collectd_plugin_namesL = [
        "match_BCH-KRW",
        "trade_BCH-KRW",
        "match_BOS-GT",
        "trade_BOS-GT",
        "match_BOS-KRW",
        "trade_BOS-KRW",
        "match_BSV-KRW",
        "trade_BSV-KRW",
        "match_BTC-KRW",
        "trade_BTC-KRW",
        "match_CMT-KRW",
        "trade_CMT-KRW",
        "match_COSM-KRW",
        "trade_COSM-KRW",
        "match_DASH-KRW",
        "trade_DASH-KRW",
        "match_ENJ-GT",
        "trade_ENJ-GT",
        "match_ENJ-KRW",
        "trade_ENJ-KRW",
        "match_ETC-KRW",
        "trade_ETC-KRW",
        "match_ETH-GT",
        "trade_ETH-GT",
        "match_ETH-KRW",
        "trade_ETH-KRW",
        "match_GT-KRW",
        "trade_GT-KRW",
        "match_HDAC-KRW",
        "trade_HDAC-KRW",
        "match_HOT-KRW",
        "trade_HOT-KRW",
        "match_LTC-KRW",
        "trade_LTC-KRW",
        "match_MITH-KRW",
        "trade_MITH-KRW",
        "match_OMG-KRW",
        "trade_OMG-KRW",
        "match_PCH-KRW",
        "trade_PCH-KRW",
        "match_RDN-KRW",
        "trade_RDN-KRW",
        "match_SNT-KRW",
        "trade_SNT-KRW",
        "match_UPP-KRW",
        "trade_UPP-KRW",
        "match_WGP-GT",
        "trade_WGP-GT",
        "match_WGP-KRW",
        "trade_WGP-KRW",
        "match_XLM-KRW",
        "trade_XLM-KRW",
        "match_XRP-GT",
        "trade_XRP-GT",
        "match_XRP-KRW",
        "trade_XRP-KRW",
        "match_ZEC-KRW",
        "trade_ZEC-KRW",
        "match_ZRX-KRW",
        "trade_ZRX-KRW"
    ]

    for pname in collectd_plugin_namesL:
        resp = create_collectd_process_alarm(cwClient, 'match0',
                                             sns_match0, iid_match0_svr,
                                             pname)
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("SUCCESS! Process Alarm for %s created" % pname)
        else:
            print("FAILURE! Process Alarm for %s not created" % pname)

    end = time.time()
    print("Script ran in %s seconds" % (end- start))


if __name__ == "__main__":
    main()
