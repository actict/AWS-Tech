#!/bin/bash
# admin-combined_loglevel_error_mkII.sh
#
# Last Updated: 2019.05.24
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel '[ERROR]' events for both
# admin-front (SHD) and admin-access (API). If results exist, they
# will be sent to the slack channel 'notify_admin' This script is
# intended to be run at regular intervals by a cron script or systemd
# timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="admin-tonghap_logs"
filterp='[loglevel=error, ID, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-150 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/admin-access-loglevel_error.log"
logfile="$appfolder/get_cw_logs_admin-combined.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="admin-access loglevel:error!"


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

# Define 2nd filterp, resultf and subj for 'admin-front nginx errors'
filterp='[YYYYMMDD, hhmmss, loglevel=error || loglevel=crit || loglevel=alert || loglevel=emerg, pid, msg]'
resultf="$appfolder/admin-front_nginx-error-events.log"
subj="admin-front nginx error.log event!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
