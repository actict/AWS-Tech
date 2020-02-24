#!/bin/bash
# rds_cloudwatch_log_query_tonghap_mkII.sh
#
# Last Updated: 2019.07.26
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to check for RDS error and slow query logs with
# various filter patterns. Errors will be sent to Slack channel
# '#notify_db', while slow queries will be sent to '#notify_slowquery'
# This script is intended to be run at regular intervals by a cron
# script or systemd timer (preferred).
#
# NOTE: This script separately queries log streams from the log
# groups:
#
# - '/aws/rds/cluster/prod-db-phoenix/error'
# - '/aws/rds/cluster/prod-db-phoenix/slowquery'
#
# and within these log groups the following log streams:
#
# - 'prod-db-phoenix'
# - 'prod-db-phoenix-ap-northeast-2c'
#
# NOTE 2019.07.26 added a new filter script:
# - 'get_cloudwatch_logs_RDS_except_alrime_wo_tmstmp.py'
# which will be used in addition to 'get_cloudwatch_logs.py' and
# 'get_cloudwatch_logs_except_alrime.py'


appfolder="/home/ec2-user/bin"
awsenvo='prod_cw_logs_ro'

#### QUERY 1 ####
log_grp="/aws/rds/cluster/prod-db-phoenix/error"
log_strm="prod-db-phoenix"
filterp='[date, time, proc, loglevel=*ERROR*, body]'
t_start=$(date -u +%F' '%H:%M:%S --date '-145 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-70 sec')
resultf="$appfolder/RDS_errorlog_prod-db-phoenix"
logfile="$appfolder/get_cw_logs_RDS_query_tonghap_mkII.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="RDS-Aurora 'Error Log' from 'prod-db-phoenix'!"

# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1


#### QUERY 2 ####
# define new 'log_strm', 'resultf', 'subj' for log stream
# "prod-db-phoenix-ap-northeast-2c" to check for error logs
log_strm="prod-db-phoenix-ap-northeast-2c"
resultf="$appfolder/RDS_errorlog_prod-db-phoenix-ap-ne-2c"
subj="RDS-Aurora 'Error Log' from 'prod-db-phoenix-ap-northeast-2c'!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1


#### QUERY 3 ####
# Check for slow queries where dbuser is NOT 'alrime*' which is part
# of cruizer app. Define new 'log_grp', 'log_strm', 'filterp',
# 'resultf', 'subj' for log stream 'prod-db-phoenix' and 'slack_webhook'
# to send results to Slack channel '#notify_slowquery'
log_grp="/aws/rds/cluster/prod-db-phoenix/slowquery"
log_strm="prod-db-phoenix"
filterp='[f1, timeHdr, yymmdd, hhmmss, f4, f5, dbuser!=alrime*, f7, IP, IdHdr, Id, f11, querytHdr, querytval>10, lockt, locktval, RowSentHdr, RowSent, RowsExamHdr, RowsExam, queryBody]'
resultf="$appfolder/RDS_slow_query_prod-db-phoenix.log"
subj="RDS-Aurora 'SLOW QUERY' from 'prod-db-phoenix'!"
slack_webhook="https://hooks.slack.com/services/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"

python3 "$appfolder"/get_cloudwatch_logs_RDS_except_alrime.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1


#### QUERY 4 ####
# Check for slow queries where dbuser is NOT 'alrime*' which is part
# of cruizer app. Define new 'log_strm', 'resultf', 'subj' for log
# stream 'prod-db-phoenix-ap-northeast-2a'
log_strm="prod-db-phoenix-ap-northeast-2c"
resultf="$appfolder/RDS_slow_query_prod-db-phoenix-ap-northeast-2c.log"
subj="RDS-Aurora 'SLOW QUERY' from 'prod-db-phoenix-ap-northeast-2c'!"
slack_webhook="https://hooks.slack.com/services/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"

python3 "$appfolder"/get_cloudwatch_logs_RDS_except_alrime.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1


#### QUERY 5 ####
# Check for slow queries where dbuser is NOT 'alrime*' which is part
# of cruizer app. Define new 'log_grp', 'log_strm', 'filterp',
# 'resultf', 'subj' for log stream 'prod-db-phoenix' and 'slack_webhook'
# to send results to Slack channel '#notify_slowquery'
#
# NOTE: The query pattern for dbuser 'alrime' changed on 2019.07.15 at
# around 11:30 AM, making the old filter pattern unable to parse the
# new 'alrime' queries from cruiser. I therefore created a new query
# pattern below to match new 'alrime' queries
log_grp="/aws/rds/cluster/prod-db-phoenix/slowquery"
log_strm="prod-db-phoenix"
filterp='[h2, host, dbuser!=alrime*, snail, IP, idheader, id, h3, qtimeheader, qtime>10, ltimeheader, ltime, rowsHdr, rowsVal, rowsExam, rowsExamVal, querybody]'
resultf="$appfolder/RDS_slow_query_prod-db-phoenix.log"
subj="RDS-Aurora 'SLOW QUERY' from 'prod-db-phoenix'!"
slack_webhook="https://hooks.slack.com/services/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"

python3 "$appfolder"/get_cloudwatch_logs_RDS_except_alrime_wo_tmstmp.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

#### QUERY 6 ####
# Check for slow queries where dbuser is NOT 'alrime*' which is part
# of cruizer app. Define new 'log_grp', 'log_strm', 'filterp',
# 'resultf', 'subj' for log stream 'prod-db-phoenix' and 'slack_webhook'
# to send results to Slack channel '#notify_slowquery'
#
# NOTE: The query pattern for dbuser 'alrime' changed on 2019.07.15 at
# around 11:30 AM, making the old filter pattern unable to parse the
# new 'alrime' queries from cruiser. I therefore created a new query
# pattern below to match new 'alrime' queries
log_grp="/aws/rds/cluster/prod-db-phoenix/slowquery"
log_strm="prod-db-phoenix-ap-northeast-2c"
filterp='[h2, host, dbuser!=alrime*, snail, IP, idheader, id, h3, qtimeheader, qtime>10, ltimeheader, ltime, rowsHdr, rowsVal, rowsExam, rowsExamVal, querybody]'
resultf="$appfolder/RDS_slow_query_prod-db-phoenix.log"
subj="RDS-Aurora 'SLOW QUERY' from 'prod-db-phoenix'!"
slack_webhook="https://hooks.slack.com/services/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"

python3 "$appfolder"/get_cloudwatch_logs_RDS_except_alrime_wo_tmstmp.py "$awsenvo" \
        "$log_grp" "$filterp" "$t_start" "$t_end" "$resultf" "$logfile" \
        --logstreams "$log_strm"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf results to Slack... ###"
  python3 "$appfolder"/send_to_slack_webhook_mkII.py "$resultf" \
          "$slack_webhook" "$subj"
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
