#!/bin/bash
# aide_file_integrity_alert.sh
#
# Last Updated: 2019.09.15
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs_print_logstream_name.py' and
# runs a query against AWS Cloudwatch Logs to find all AIDE file
# change events from the log group 'all_aide_logs'.  If results exist,
# they will be sent to the slack channel 'notify_무결성'. This script
# is intended to be run at regular intervals by a systemd timer
# (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs+print_logstream_name.py ###
awsenvo='prod_cw_logs_ro'
log_grp="all_aide_logs"
filterp='"found differences between database and filesystem!!"'
t_start=$(date -u +%F' '%H:%M:%S --date '-150 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/aide_file_integrity_results.log"
logfile="$appfolder/aide_file_integrity_app_log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook=$(<"$appfolder/slack_notify_aide")
subj="AIDE File Integrity Changes!"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs_print_logstream_name.py \
        "$awsenvo" "$log_grp" "$filterp" "$t_start" "$t_end" \
        "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
