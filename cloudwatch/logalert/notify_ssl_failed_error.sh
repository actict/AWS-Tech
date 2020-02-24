#!/bin/bash
# notify_ssl_failed_error_mkII.sh
#
# Last Updated: 2019.10.02
# Updated by: scott.hwang@peertec.com #
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find gdac.com website login errors from the
# API server log (prod-access Elastic Beanstalk). If results exist,
# they will be sent to the slack channel 'notify_weblogin'. This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="$HOME/Documents/SecOps-Documents/AWS/boto3"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="genesis_logs"
# filter pattern to find ansible playbook errors
filterp='[MM, DD, timestamp, hostname, systemd, msg="Failed to start Run ansible playbook*"]'
t_start=$(date -u +%F' '%H:%M:%S --date '-120 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/prod-notify_ssl_failed_error"
logfile="$appfolder/get_cw_logs_prod-ssl_ansibleplaybook_error.log"
slack_webhook="https://hooks.slack.com/services/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"
subj="SSL ansible-playbook FAIL ERROR"


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
