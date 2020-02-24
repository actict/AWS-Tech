#!/bin/bash
# notify_weblogin_prod_access_error_mkII.sh
#
# Last Updated: 2019.09.06
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find gdac.com website login errors from the
# API server log (prod-access Elastic Beanstalk). If results exist,
# they will be sent to the slack channel 'notify_weblogin'. This
# script is intended to be run at regular intervals by a cron script
# or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###
awsenvo='prod_cw_logs_ro'
log_grp="prod-access_logs"
# filter pattern to find max OTP auth erros
filterp='[loglevel=info, svr, iid, timestamp, type, num, uuid, ip, custID, name, reqType, endpt, code=400, msg="*auth_otp_attempts_over*"]'
t_start=$(date -u +%F' '%H:%M:%S --date '-61 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-1 sec')
resultf="$appfolder/prod-access_notify_weblogin_otp"
logfile="$appfolder/get_cw_logs_prod-access_login_error.log"
slack_webhook=$(<"$appfolder/slack_notify_weblogin_webhook")
subj="GDAC Login OTP max tries exceeded!"


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

# Define 2nd filterp, resultf and subj for 'auth_email_login' PW errors
filterp='[loglevel=error, svr, iid, timestamp, module=auth_email_login, msg="*__cipher_not_identical_*"]'
resultf="$appfolder/prod-access_notify_weblogin_email_badPW"
subj="GDAC Login email bad PW!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
