#!/bin/bash
# auth-combined_loglevel_error_mkII.sh
#
# Last Updated: 2019.01.15
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel '[ERROR]' events from all
# auth-related log groups. If results exist, they will be sent to the slack
# channel 'notify_auth' This script is intended to be run at regular
# intervals by a cron script or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="auth-bank_logs"
filterp='[loglevel=ERROR, ID, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-150 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/auth-bank-loglevel_error.log"
logfile="$appfolder/get_cw_logs_auth-combined.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="auth-bank loglevel:ERROR!"

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

sleep 1


# define new 'log_grp', 'filterp', 'resultf', and 'subj' for
# auth-phone server
log_grp="auth-phone_logs"
filterp='[loglevel=ERROR, ID, timestamp, msg]'
resultf="$appfolder/auth-phone-loglevel_error.log"
### args for send_to_slack_webhook_mkII.py ###
subj="auth-phone loglevel:ERROR!"

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


# define new 'log_grp', 'filterp', 'resultf', and 'subj' for
# auth-kakaopay server
log_grp="auth-kakaopay_logs"
filterp='[loglevel=WARN, ID, timestamp, msg]'
resultf="$appfolder/auth-kakaopay-loglevel_warn.log"
### args for send_to_slack_webhook_mkII.py ###
subj="auth-kakaopay loglevel:WARN!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
