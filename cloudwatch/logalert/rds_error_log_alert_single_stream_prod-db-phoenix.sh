#!/bin/bash
# rds_error_log_alert_single_stream_prod-db-phoenix.sh
#
# Last Updated: 2018.12.09
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs for RDS error log with a filter pattern that
# will only return log level [ERROR] or 'InnoDB: Error' If such
# records exist, they will be sent to the slack channel 'notify_db'
# This script is intended to be run at regular intervals by a cron
# script or systemd timer (preferred).
#
# NOTE: This script only queries a single log stream 'prod-db-phoenix'
# from the log group '/aws/rds/cluster/prod-db-phoenix/error',
# log stream 'prod-db-phoenix'

appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="/aws/rds/cluster/prod-db-phoenix/error"
log_strm="prod-db-phoenix"
filterp='[date, time, proc, loglevel=*ERROR*, body]'
t_start=$(date -u +%F' '%H:%M:%S --date '-135 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-70 sec')
resultf="$appfolder/RDS_errorlog_prod-db-phoenix"
logfile="$appfolder/get_cw_logs_RDS_errorlog_prod-db-phoenix.log"
### args for smtp-cli ###
slack_email="f9x3u6h7i0w2e0m4@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="RDS-Aurora 'Error Log' from 'prod-db-phoenix'!"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

# check for smtp-cli in $appfolder
if [ -f "$appfolder"/smtp-cli ]; then
  :
else
  printf "%s\\n" "### smtp-cli not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\\n" "### No results to send right now ###"
fi

# Define second filter pattern and mailsubj for 'InnoDB Error'
filterp='[date, time, proc, InnoDB, loglevel=Error*, body]'
resultf="$appfolder/RDS_errorlog_InnoDB_error_prod-db-phoenix"
mailsubj="RDS-Aurora 'InnoDB Error' from 'prod-db-phoenix'!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\\n" "### No results to send right now ###"
fi
