#!/usr/bin/env bash
# update_aws_envo_profile.sh
#
# Last Updated: 2019.05.24
# Updated by: scott.hwang@peertec.com
#
# This script will replace the value for 'awsenvo' in cloudwatch
# log query scripts running on 'logger' server. Note that when you
# pass the first and second arguments to this program, you need
# to use two quote levels to preserve the inner single-quotes, i.e.
#
# "'prod'"
# "'prod_cw_logs_ro'"

curr_awsenvo="$1"
update_awsenvo="$2"
path_to_files="$3"

filesList=(
  "$path_to_files"/access-gdac-beta_loglevel_error.sh
  "$path_to_files"/access-gdac_loglevel_error.sh
  "$path_to_files"/admin-access_loglevel_error.sh
  "$path_to_files"/admin-combined_loglevel_error_mkII.sh
  "$path_to_files"/auth-bank_loglevel_error.sh
  "$path_to_files"/auth-combined_loglevel_error_mkII.sh
  "$path_to_files"/auth-kakaopay_loglevel_warn.sh
  "$path_to_files"/auth-phone_loglevel_error.sh
  "$path_to_files"/chart-pub_loglevel_error.sh
  "$path_to_files"/chart-svr_loglevel_error_mkII.sh
  "$path_to_files"/chart-svr_loglevel_error.sh
  "$path_to_files"/cloudtrail_errors_mkII.sh
  "$path_to_files"/cloudtrail_errors.sh
  "$path_to_files"/cruiser_loglevel_ERROR_mkII.sh
  "$path_to_files"/ledger_loglevel-error_mkII.sh
  "$path_to_files"/ledger_loglevel-error.sh
  "$path_to_files"/match0_loglevel-error.sh
  "$path_to_files"/match0_status_day-change.sh
  "$path_to_files"/notifier-prod_loglevel_error.sh
  "$path_to_files"/openapi-gdac_loglevel-error.sh
  "$path_to_files"/openapi_internal_error.sh
  "$path_to_files"/order-pub_loglevel_error.sh
  "$path_to_files"/order-svr_loglevel_error.sh
  "$path_to_files"/prod-access_log_alert_internal_error_mkII.sh
  "$path_to_files"/prod-access_log_alert_internal_error.sh
  "$path_to_files"/prod-access_log_alert_notify_fds_mkII.sh
  "$path_to_files"/prod-access_log_alert_notify_fds.sh
  "$path_to_files"/prod-access_log_alert.sh
  "$path_to_files"/prod-front_cloudwatch_log_error_noti_mkII.sh
  "$path_to_files"/rds_cloudwatch_log_query_tonghap_mkII.sh
  "$path_to_files"/rds_error_log_alert_single_stream_prod-db-phoenix-ap-ne-2c.sh
  "$path_to_files"/rds_error_log_alert_single_stream_prod-db-phoenix.sh
  "$path_to_files"/slow_query_log_alert.sh
  "$path_to_files"/slow_query_log_alert_single_stream_prod-db-phoenix-ap-ne-2c.sh
  "$path_to_files"/slow_query_log_alert_single_stream_prod-db-phoenix.sh
  "$path_to_files"/wallet_loglevel-error_mkII.sh
  "$path_to_files"/wallet_loglevel-error.sh
)


if [ $# -ne 3 ]; then
  printf "%s\\n" "### This program requires 3 arguments ###"
  printf "%s\\n" "(1) current value of 'awsenvo'"
  printf "%s\\n" "(2) new value of 'awsenvo'"
  printf "%s\\n" "(3) path to files to be edited"
  exit 1
fi

for myfile in "${filesList[@]}"; do
  printf "%s\\n" "Updating 'awsenvo' in $myfile..."
  sed -i "s:awsenvo=$curr_awsenvo:awsenvo=${update_awsenvo}:g" "$myfile"
done
