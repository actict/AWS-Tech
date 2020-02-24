#!/bin/bash
# chatbot_monitor_cloudwatch_log_query_mkII.sh
#
# Last Updated: 2019.06.23
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch log streams corresponding to chatting channels on
# discord, telegram, matrix.org, etc. Filter patterns for each log
# stream within the Log Group 'maintenance-server_logs' try to match
# keywords related to Software Updates for various blockchain projects
# including COSMOS, Terra LUNA, Irisnet, Cybermiles CMT, etc. If a
# match is found, the chat log containing the match will be sent to
# the Slack channel '#notify_bchain_updates'. This script is intended
# to be run at regular intervals by a cron script or systemd timer
# (preferred).


appfolder="/home/ec2-user/bin"
awsenvo='prod_cw_logs_ro'

#### QUERY 1 ####
log_grp="maintenance-server_logs"
log_strm="terra-vali-SW-updates_10.0.33.14_chat.log"
filterp='[HrMin, delim, nick, user, msg=*upgrade* || msg=*update || msg=*new]'
t_start=$(date -u +%F' '%H:%M:%S --date '-310 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-10 sec')
resultf="$appfolder/terra-vali-sw-updates-match"
logfile="$appfolder/get_cw_logs_chatbot_monitor_mkII.log"
### args for send_to_slack_webhook_mkII.py ###
slack_webhook="https://hooks.slack.com/services/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"
subj="Terra Validator Update News!"

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

#### QUERY 2 ####
# define new 'log_strm', 'resultf', 'subj' for log stream
# "irisTechUpdates_10.0.33.14_chat.log" to check for updates
filterp='[HrMin, delim, nick, user, msg=*upgrade* || msg=*update || msg=*new]'
log_strm="irisTechUpdates_10.0.33.14_chat.log"
resultf="$appfolder/iris-technical-updates-match"
subj="Irisnet Technical Updates News!"

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
# define new 'log_strm', 'resultf', 'subj' for log stream
# "iris-validators_10.0.33.14_chat.log" to check for updates.s
# Note the filterp for 'iris-validators' channel is slightly
# different from that of 'irisTechUpdates'; '*update*' vs '*update'
filterp='[HrMin, delim, nick, user, msg=*upgrade* || msg=*update* || msg=*new]'
log_strm="iris-validators_10.0.33.14_chat.log"
resultf="$appfolder/iris-validators-match"
subj="Irisnet Validators Update News!"

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

#### QUERY 4 ####
# define new 'log_strm', 'filterp', 'resultf', 'subj' for log stream
# "cosmos-validators_10.0.33.14_chat.log" to check for updates
filterp='[HrMin, nick, msg=*upgrade* || msg=*update*]'
log_strm="cosmos-validators_10.0.33.14_chat.log"
resultf="$appfolder/cosmos-validators-updates-match"
subj="COSMOS Validators Update News!"

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

#### QUERY 5 ####
# define new 'log_strm', 'filterp', 'resultf', 'subj' for log stream
# "cmt-validators_10.0.33.14_chat.log" to check for updates
filterp='[HrMin, nick, msg=*update* || msg=*upgrade*]'
log_strm="cmt-validators_10.0.33.14_chat.log"
resultf="$appfolder/cmt-validators-match"
subj="Cybermiles Validators Update News!"

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

#### QUERY 6 ####
# define new 'log_strm', 'filterp', 'resultf', 'subj' for log stream
# "cosmos-tech-updates_10.0.33.14_chat.log" to check for updates
filterp='[HrMin, nick, msg=*update* || msg=*upgrade*]'
log_strm="cosmos-tech-updates_10.0.33.14_chat.log"
resultf="$appfolder/cosmos-tech-updates-match"
subj="Cosmos Tech Updates News!"

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

#### QUERY 7 ####
# define new 'log_strm', 'filterp', 'resultf', 'subj' for log stream
# "terra-vali-announce_10.0.33.14_chat.log" to check for updates
filterp='[HrMin, nick, msg=*update* || msg=*upgrade*]'
log_strm="terra-vali-announce_10.0.33.14_chat.log"
resultf="$appfolder/terra-vali-announce-match"
subj="Terra Validator Update News!"

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
