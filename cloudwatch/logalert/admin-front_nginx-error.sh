#!/bin/bash
# admin-front_nginx-error.sh
#
# Last Updated: 2018.12.26
# Updated by: scott.hwang@peertec.com and joshua.huh@actwo.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs for nginx error.log and returns events. for
# loglevels 'error', 'crit', 'alert', and 'emerg'. If results exist,
# they will be sent to the slack channel 'notify_admin' This script
# is intended to be run at regular intervals by a cron script or
# systemd timer (preferred).
#
# THIS SCRIPT IS DEPRECATED; USE admin-combined_loglevel_error_mkII.sh
# instead.


appfolder="/home/ec2-user/bin"
awsenvo="prod"
log_grp="admin-front_logs"

### filter patterns for various nginx 'error.log' loglevels
errorp='[YYYYMMDD, hhmmss, loglevel=error, pid, msg]'
critp='[YYYYMMDD, hhmmss, loglevel=crit, pid, msg]'
alertp='[YYYYMMDD, hhmmss, loglevel=alert, pid, msg]'
emergp='[YYYYMMDD, hhmmss, loglevel=emerg, pid, msg]'

# array of all filter patterns
IFS=$'\n'
allFilters=($errorp
            $critp
            $alertp
            $emergp
            )

t_start=$(date -u +%F' '%H:%M:%S --date '-181 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-91 sec')
resultf="$appfolder/admin-front_nginx-error-events.log"
logfile="$appfolder/get_cw_logs_admin-front_nginx_error.log"
### args for smtp-cli ###
slack_email="z4c7z8d0h8e6r8p3@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="admin-front nginx error.log event!"


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

for fpattern in ${allFilters[*]}; do
  python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
          "$fpattern" "$t_start" "$t_end" "$resultf" "$logfile"

  if [ -s "$resultf" ]; then
    "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                --user=$mailuser --pass="$mailpw" --from=$mailuser \
                --to=$slack_email  --subject="$mailsubj" \
                --body-plain="$resultf" --charset=UTF-8
  else
    printf "%s\n" "### No results to send right now ###"
  fi
done
