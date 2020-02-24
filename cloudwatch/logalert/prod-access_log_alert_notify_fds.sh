#!/bin/bash
# prod-access_log_alert_notify_fds.sh
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find suspicious events from the API server
# log (prod-access Elastic Beanstalk). If results exist, they will be
# sent to the slack channel 'notify_fds' This script is intended to
# be run at regular intervals by a cron script or systemd timer
# (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="prod-access_logs"
filterp='[loglevel, access, iid, timestamp, type=RES, num, uuid, ip, custID, name, action, endpoint, httpcode!=200 && httpcode!=304 && httpcode!=302, body]'
t_start=$(date -u +%F' '%H:%M:%S --date '-120 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/prod-access_RES_suspicious"
logfile="$appfolder/get_cw_logs_prod-access_log_alert.log"
### args for smtp-cli ###
slack_email="e2u2h1m8a9p6x5f8@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="prod-access RES not 200, 302, 304!"


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

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\\n" "### No results to send right now ###"
fi
