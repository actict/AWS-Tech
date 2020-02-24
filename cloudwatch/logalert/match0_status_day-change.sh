#!/bin/bash
# match0_status_day-change.sh
#
# Last Updated: 2018.10.04
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query
# against AWS Cloudwatch Logs to find all log events that
# match a filter pattern containing "day change event". If results
# exist, these results will be sent to the slack channel 'notify_match0'
# This script is intended to be run at regular intervals by a cron
# script.


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="match0_logs"
filterp='[result=STATUS, ID, app, timestamp, fs1, fs2, msg="day change event processed"]'
t_start=$(date -u +%F' '%H:%M:%S --date '-2 min')
t_end=$(date -u +%F' '%H:%M:%S --date '-1 min')
resultf="$appfolder/match0_day_change.log"
logfile="$appfolder/get_cw_logs_match0_day-change.log"
### args for smtp-cli ###
slack_email="i1v0b5g1k4a9k8k7@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="match0 DAY CHANGE EVENT PROCESSED"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

# check for smtp-cli in $appfolder
if [ -f "$appfolder"/smtp-cli ]; then
  :
else
  printf "%s\n" "### smtp-cli not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
              --user=$mailuser --pass="$mailpw" --from=$mailuser \
              --to=$slack_email --subject="$mailsubj" \
              --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\n" "### No results to send right now ###"
fi
