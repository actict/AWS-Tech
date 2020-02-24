#!/bin/bash
# ssh_login_error_alert_mkII.sh
#
# Last Updated: 2019.08.19
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all ssh log 'error' events for all EC2
# instances (including Elastic Beanstalk). Any time an error log line is
# detected, it is sent to the slack channel 'notify_ssh'. This script is
# intended to be run at regular intervals by a cron script or systemd
# timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="all_ssh_logs"
filterp='[MM, DD, hhmmss, hostname, service=sshd*, msg=error*]'
t_start=$(date -u +%F' '%H:%M:%S --date '-70 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-10 sec')
resultf="$appfolder/ssh_error.log"
logfile="$appfolder/ssh_login_alert.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="SSH Login Error Detected!"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\nn" "### python3 not installed! Install it and try again ###"
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
