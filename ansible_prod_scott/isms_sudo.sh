#!/bin/bash
# isms_sudo.sh
#
# Last Updated: 2020.02.19
# Updated by: scott.hwang@peertec.com


mode="$1"

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
    ansible-playbook isms_diagnosis.yaml -i hosts_isms -e "myhost=mgmt_sudo"
elif [ "$mode" = "check" ]; then
    ansible-playbook isms_diagnosis.yaml --check \
                     -i hosts_isms -e "myhost=dev_sudo"
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
