#!/bin/bash
# wallet_loglevel-error.sh
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all loglevel 'ERROR' events If results
# exist, they will be sent to the slack channel 'notify_wallet' This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="wallet-svr_logs"
filterp='[result=ERROR, wallet, app, timestamp, msg]'
t_start=$(date -u +%F' '%H:%M:%S --date '-130 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-1 min')
resultf="$appfolder/wallet_error.log"
logfile="$appfolder/get_cw_logs_wallet-error.log"
### args for smtp-cli ###
slack_email="p3f2j8o2h7i1u1r0@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="wallet loglevel:ERROR!"


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
  $appfolder/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 2nd filterp, resultf and mailsubj for 'TypeError'
filterp='TypeError'
resultf="$appfolder/wallet_TypeError.log"
mailsubj="wallet TypeError!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 3rd filterp, resultf and mailsubj for 'File'
filterp='File'
resultf="$appfolder/wallet_error_trace_File.log"
mailsubj="wallet Error Trace - File!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 4th filterp, resultf and mailsubj for 'Traceback'
filterp='Traceback'
resultf="$appfolder/wallet_error_traceback.log"
mailsubj="wallet Error Traceback!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 5th filterp, resultf and mailsubj for '__init__.py'
filterp='init'
resultf="$appfolder/wallet_error_trace_init.log"
mailsubj="wallet Error Trace - init!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
