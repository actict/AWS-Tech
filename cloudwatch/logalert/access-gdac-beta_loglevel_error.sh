#!/bin/bash
# access-gdac-beta_loglevel_error.sh
#
# Last Updated: 2018.10.05
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel '[error]' events. If results
# exist, they will be sent to the slack channel 'notify_access' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="acc-gdac-beta_logs"
filterp='[loglevel=error, ID, instID, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-181 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-91 sec')
resultf="$appfolder/access-gdac-beta_error.log"
logfile="$appfolder/get_cw_logs_access-gdac_error.log"
### args for smtp-cli ###
slack_email="c9p7u1f9k1l7s0y7@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="access-gdac-BETA loglevel:error!"


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
