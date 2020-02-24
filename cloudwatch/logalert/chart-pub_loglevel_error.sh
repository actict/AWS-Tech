#!/bin/bash
# chart-pub_loglevel_error.sh
#
# Last Updated: 2019.05.29
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel '[ERROR]' events. If results
# exist, they will be sent to the slack channel 'notify_order_chart' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="chart-pub_logs"
filterp='[loglevel=ERROR, ID, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-130 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/chart-pub-loglevel_error.log"
logfile="$appfolder/get_cw_logs_chart-pub_error.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="chart-pub loglevel:ERROR!"

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
  printf "%s\\n" "### Sending $resultf to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No results to send right now ###"
fi
