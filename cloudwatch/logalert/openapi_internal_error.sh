#!/bin/bash
# openapi-internal_error.sh
#
# Last Updated: 2019.05.29
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cw_logs_oapi_internal_error.py' and runs
# a query against AWS Cloudwatch Logs to find the string
# '__internal_error__' from loglevel '[info]' events. If results
# exist, they will be sent to the slack channel 'notify_oapi' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="openapi-gdac_logs"
filterp='[loglevel=info, ID, instID, timestamp, type, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-140 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-70 sec')
resultf="$appfolder/openapi-gdac_internal_error.log"
logfile="$appfolder/get_cw_logs_oapi_internal_error.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="openapi __internal_error__!"

# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cw_logs_oapi_internal_error.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No results to send right now ###"
fi
