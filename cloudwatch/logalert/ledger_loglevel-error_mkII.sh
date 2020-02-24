#!/bin/bash
# ledger_loglevel-error_mkII.sh
#
# Last Updated: 2019.07.10
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel 'error' events for the
# ledger (dcq) server. If results exist, they will be sent to the
# slack channel 'notify_db' This script is intended to be run at
# regular intervals by a cron script or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="ledger_logs"
filterp='[loglevel=error, ID, timestamp, nonce, msg !="*order_insufficient_balance*" && msg !="*order_blocked_user*" && msg !="*order_already_closed*"]'
t_start=$(date -u +%F' '%H:%M:%S --date '-140 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/ledger_loglevel-error.log"
logfile="$appfolder/get_cw_logs_ledger_loglevel-error_mkII.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="ledger loglevel:ERROR!"


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

# Define 2nd filterp, resultf and subj for loglevel [info]
# containing '__internal_error__' in json body
filterp='[loglevel=info, db, timestamp, transNo, dash, action, msg=*internal*]'
resultf="$appfolder/ledger_loglevel-info_internalError.log"
subj="!!ledger __internal_error__"

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

# Define 3nd filterp, resultf and subj for loglevel [warn]
# containing '__unknown_error__' in json body
filterp='[loglevel=warn, db, timestamp, uuid, dash, msg=*unknown*]'
resultf="$appfolder/ledger_loglevel-info_unknownError.log"
subj="!!ledger __unknown_error__"

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

# Define 4th logstream, filterp, resultf and subj for PM2 resurrect
# event from syslog logstream in ledger_logs log group
filterp='[MTH, DAY, HHMMSS, host, service=pm2*, msg=*Resurrecting*]'
log_strm="ledger_10.0.48.128_var_log_messages"
resultf="$appfolder/ledger_pm2_resurrect.log"
subj="!!ledger PM2 restarted!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
