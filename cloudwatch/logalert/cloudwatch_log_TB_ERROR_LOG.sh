#!/usr/bin/env bash
# cloudwatch_log_TB_ERROR_LOG.sh
#
# Last Updated: 2019.02.14
# Updated by: scott.hwang@peertec.com
#
# This script is intended to be run by a systemd service and
# timer file combo. It executes logalert_whalex_TB_ERROR_LOG.py
# with appropiate parameters.

python3 /home/ec2-user/bin/logalert_whalex_TB_ERROR_LOG.py backup_whalex.TB_ERROR_LOG
