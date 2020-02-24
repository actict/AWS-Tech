#!/bin/bash
# prod-access_log_alert_notify_fds_mkII.sh
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find suspicious events from the API server
# log (prod-access Elastic Beanstalk). If results exist, they will be
# sent to the slack channel 'notify_fds' This script is intended to
# be run at regular intervals by a cron script or systemd timer
# (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="prod-access_logs"
filterp='[loglevel, access, iid, timestamp, type=RES, num, uuid, ip, custID, name, action, endpoint, httpcode!=200 && httpcode!=304 && httpcode!=302, body]'
t_start=$(date -u +%F' '%H:%M:%S --date '-120 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/prod-access_RES_suspicious_mkII"
logfile="$appfolder/get_cw_logs_prod-access_log_alert_mkII.log"
### args for send_to_slack_webhook_mkII.py  ###
slack_webhook='https://hooks.slack.com/services/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'
subj="prod-access RES not 200, 302, 304!"


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
