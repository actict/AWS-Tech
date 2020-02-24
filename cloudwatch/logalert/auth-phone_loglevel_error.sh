#!/bin/bash
# auth-phone_loglevel_error.sh
#
# Last Updated: 2018.12.26
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel '[ERROR]' events. If results
# exist, they will be sent to the slack channel 'notify_auth' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).
#
# This script is DEPRECATED and auth-combined_loglevel_error_mkII.sh
# should be used instead.


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="auth-phone_logs"
filterp='[loglevel=ERROR, ID, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-150 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/auth-phone-loglevel_error.log"
logfile="$appfolder/get_cw_logs_auth-phone_error.log"
### args for smtp-cli ###
slack_email="m1t4t9d6g0q6m7a3@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="auth-phone loglevel:ERROR!"


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
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\n" "### No results to send right now ###"
fi
