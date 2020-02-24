#!/bin/bash
# match0_asset_pair_process_alarm_count.sh
#
# Last Updated: 2019.05.24
# Updated by: scott.hwang@peertec.com
#
# This wrapper invokes match0_asset_pair_process_alarm_count_checker.py
# with its sole argument awscli/boto3 'profile_name' which gives
# read-only access to Cloudwatch Alarms

python3 /home/ec2-user/bin/match0_asset_pair_process_alarm_count_checker.py \
        prod_cw_ro
