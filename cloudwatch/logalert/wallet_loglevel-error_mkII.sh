#!/bin/bash
# wallet_loglevel-error_mkII.sh
#
# Last Updated: 2019.06.09
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel 'ERROR' events If results
# exist, they will be sent to the slack channel 'notify_wallet' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred). It uses the custom AWS IAM role
# defined by Hashicorp Vault, 'wallet-log-monitor' which provides
# access to the following AWS policies:
#
# - arn:aws:iam::762015387773:policy/sns-publish-all-topics
# - arn:aws:iam::aws:policy/CloudWatchLogsReadOnlyAccess


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_ro_sns_pub'
log_grp="wallet-svr_logs"
filterp='[result=ERROR, wallet, app, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-125 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-1 min')
resultf="$appfolder/wallet_error_mkII.log"
logfile="$appfolder/get_cw_logs_wallet-error_mkII.log"
### args for slack ###
subj="wallet loglevel:ERROR!"
slack_webhook=https://hooks.slack.com/services/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


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

# check for pdagent
if [ -f /usr/bin/pd-send ]; then
  :
else
  printf "%s\\n" "### pdagent not installed! Install it and try again ###"
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

#############################################################
# Define new filterp, resultf and subj for ATOM getBlock error
filterp='[result=ERROR, wallet, app, timestamp, msg="ATOM : getBlockNumber failed"]'
resultf="$appfolder/wallet_ATOM_getBlockNumber_failed_mkII.log"
subj="wallet ATOM getBlock failed for 5 minutes!"
slack_emergency=https://hooks.slack.com/services/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
SERVICE_KEY=$(</home/ec2-user/.pagerduty/SERVICE_KEY)
cosmos_err_cnt="$appfolder/ATOM_error.cnt"
err_cnt=$(wc -l ${cosmos_err_cnt} | awk -F ' ' '{print $1}')

touch $cosmos_err_cnt

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  if [ "$err_cnt" -gt 5 ]; then
    printf "%s\\n" "### Sending $resultf results to Slack... ###"
    python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
            "$slack_emergency" "$subj"
    printf "%s\\n" "### Sending alert to Pagerduty... ###"
    pd-send -k "$SERVICE_KEY" -t trigger \
            -d "Wallet error getting atom blocks for 5 min!"
    printf "%s\\n" "Reset $cosmos_err_cnt"
    truncate --size 0 ${cosmos_err_cnt}
  else
    printf "%s\\n" "Add line to ${cosmos_err_cnt}"
    echo "X" >> ${cosmos_err_cnt}
  fi
else
  printf "%s\\n" "### No $resultf to send right now ###"
  truncate --size 0 ${cosmos_err_cnt}
fi

sleep 1

#############################################################
# Define new filterp, resultf and subj for 'TypeError'
filterp='TypeError'
resultf="$appfolder/wallet_TypeError_mkII.log"
subj="wallet TypeError!"

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

#############################################################
# Define new filterp, resultf and subj for 'File'
filterp='File'
resultf="$appfolder/wallet_error_trace_File_mkII.log"
subj="wallet Error Trace - File!"

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

#############################################################
# Define new filterp, resultf and subj for 'Traceback'
filterp='Traceback'
resultf="$appfolder/wallet_error_traceback_mkII.log"
subj="wallet Error Traceback!"

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

#############################################################
# Define new filterp, resultf and subj for '__init__.py'
filterp='init'
resultf="$appfolder/wallet_error_trace_init_mkII.log"
subj="wallet Error Trace - init!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
