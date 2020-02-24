#!/bin/bash
# partner-api_log_alert_mkII.sh
#
# Last Updated: 2019.06.26
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find errors from the API server log
# (prod-access Elastic Beanstalk). If results exist, they will be sent
# to the slack channel 'notify_access' This script is intended to be run
# at regular intervals by a cron script or systemd timer (preferred).
# The AWS profile 'prod_cw_logs_ro' gives access to the following IAM
# policy:
#
# - CloudwatchLogsReadOnly


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="partner-api_logs"
filterp='[loglevel, appname, instanceid, timestamp, type, ver, client, method, path, res=500, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-120 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/partner-api_internal_error"
logfile="$appfolder/get_cw_logs_partner-api_internal_error.log"
### args for slack webhook script ###
slack_webhook='https://hooks.slack.com/services/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'
subj="partner-api internal error!"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

################################################
# 2019.06.26 Simon Lee wants the log filter to exclude the following
# errors:
# - "__order_insufficient_balance_"
# - "__order_already_closed_"
# - "__order_blocked_user_"

filterp='[loglevel=error, appname, iid, timestamp, msg !="*order_insufficient_balance*" && msg !="*order_blocked_user*" && msg !="*order_already_closed*"]'
resultf="$appfolder/partner-api_loglevel_error"
subj="partner-api loglevel error!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
