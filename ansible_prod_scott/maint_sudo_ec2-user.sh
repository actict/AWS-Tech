#!/bin/bash
# maint_sudo_ec2-user.sh
#
# Last Updated: 2020.01.30
# Updated by: scott.hwang@peertec.com


mode="$1"

hostL=(
  hashtower
  front-web-1
  front-web-2
  auth-bank-ng
  tx-verifier
)

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
  for h in ${hostL[*]}; do
    ansible-playbook maint_update_reboot_prod_sudo_ec2-user.yaml -i hosts -e "myhost=$h"
  done
elif [ "$mode" = "check" ]; then
  for h in ${hostL[*]}; do
    ansible-playbook maint_update_reboot_prod_sudo_ec2-user.yaml --check \
                     -i hosts -e "myhost=$h"
  done
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
