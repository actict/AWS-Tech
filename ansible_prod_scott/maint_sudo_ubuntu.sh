#!/bin/bash
# maint_sudo_ubuntu.sh
#
# Last Updated: 2020.01.30
# Updated by: scott.hwang@peertec.com


mode="$1"

hostL=(
  pay-orderbot
  peer-mysql
  peertec-web
  bip-web
  decon-web
  match
)

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
  for h in ${hostL[*]}; do
    ansible-playbook maint_update_reboot_prod_sudo_ubuntu.yaml -i hosts -e "myhost=$h"
  done
elif [ "$mode" = "check" ]; then
  for h in ${hostL[*]}; do
    ansible-playbook maint_update_reboot_prod_sudo_ubuntu.yaml --check \
                     -i hosts -e "myhost=$h"
  done
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
