#!/bin/bash
# maint_update_blockchain_reboot.sh
#
# Last Updated: 2020.02.05
# Updated by: scott.hwang@peertec.com
#
# Wrapper script to run ansible playbooks during the monthly
# maintenance job. These playbooks will update all packages on Ubuntu
# and Amazon Linux 2 servers and then reboot. Note that some servers
# have disabled "sudo" so some servers require you to enter the root
# PW on the CLI


mode="$1"

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
  printf "%s\\n" "Updating pkgs on geth1 ..."
  ansible-playbook -K maint_update_geth1.yaml
  printf "%s\\n" "Updating pkgs on geth2 ..."
  ansible-playbook -K maint_update_geth2.yaml
  printf "%s\\n" "Updating pkgs on etc ..."
  ansible-playbook -K maint_update_etc.yaml
  printf "%s\\n" "Updating pkgs on hdac ..."
  ansible-playbook -K maint_update_hdac.yaml
  printf "%s\\n" "Updating pkgs on cmt ..."
  ansible-playbook -K maint_update_cmt.yaml
  printf "%s\\n" "Updating pkgs on terra-full ..."
  ansible-playbook -K maint_update_terra_full.yaml
  printf "%s\\n" "Updating pkgs on terra-lcd ..."
  ansible-playbook -K maint_update_terra_lcd.yaml
  printf "%s\\n" "Updating pkgs on irisnet-full ..."
  ansible-playbook maint_update_irisnet_full.yaml
  printf "%s\\n" "Updating pkgs on irisnet-lcd ..."
  ansible-playbook maint_update_irisnet_lcd.yaml
  printf "%s\\n" "Updating pkgs on cosmos-lcd ..."
  ansible-playbook maint_update_cosmos_lcd.yaml
  printf "%s\\n" "Updating pkgs on wallet ..."
  ansible-playbook -K maint_update_wallet.yaml

elif [ "$mode" = "check" ]; then
  printf "%s\\n" "TEST: Updating pkgs on geth1 ..."
  ansible-playbook -K maint_update_geth1.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on geth2 ..."
  ansible-playbook -K maint_update_geth2.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on etc ..."
  ansible-playbook -K maint_update_etc.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on hdac ..."
  ansible-playbook -K maint_update_hdac.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on cmt ..."
  ansible-playbook -K maint_update_cmt.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on irisnet-full ..."
  ansible-playbook maint_update_irisnet_full.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on irisnet-lcd ..."
  ansible-playbook maint_update_irisnet_lcd.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on terra-full ..."
  ansible-playbook -K maint_update_terra_full.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on terra-lcd ..."
  ansible-playbook -K maint_update_terra_lcd.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on cosmos-lcd ..."
  ansible-playbook maint_update_cosmos_lcd.yaml --check
  printf "%s\\n" "TEST: Updating pkgs on wallet ..."
  ansible-playbook -K maint_update_wallet.yaml --check

else
    printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
