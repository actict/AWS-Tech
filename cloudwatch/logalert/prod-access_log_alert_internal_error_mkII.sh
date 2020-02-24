#!/bin/bash
# prod-access_log_alert_internal_error_mkII.sh
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find errors from the API server log
# (prod-access Elastic Beanstalk). If results exist, they will be sent
# to the slack channel 'notify_access' This script is intended to be run
# at regular intervals by a cron script or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="prod-access_logs"
filterp='[loglevel=info, access, iid, timestamp, type=RES, code, uuid, IP, custID, name, action, endpt, httpcode=500, body]'
t_start=$(date -u +%F' '%H:%M:%S --date '-120 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/prod-access_RES_internal_error_mkII"
logfile="$appfolder/get_cw_logs_prod-access_internal_error.log"
### args for smtp-cli ###
slack_webhook='https://hooks.slack.com/services/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'
subj="prod-access internal error!"


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
