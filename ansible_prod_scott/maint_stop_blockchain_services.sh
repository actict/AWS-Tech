#!/bin/bash
# maint_stop_blockchain_services.sh
#
# Last Updated: 2020.02.05
# Updated by: scott.hwang@peertec.com
#
# Wrapper script to run ansible playbooks during the monthly
# maintenance job. This script will stop blockchain related service
# daemons in the proper order to ensure that wallet server errors do
# not occur. Note that some servers have disabled "sudo" so some
# servers require you to enter the root PW on the CLI


mode="$1"

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
  ansible-playbook -K maint_stop_wallet.yaml
  printf "%s\\n" "Stopping geth service on geth1 ..."
  ansible-playbook -K maint_stop_geth1.yaml
  printf "%s\\n" "Stopping geth service on geth2 ..."
  ansible-playbook -K maint_stop_geth2.yaml
  printf "%s\\n" "Stopping geth service on etc ..."
  ansible-playbook -K maint_stop_etc.yaml
  printf "%s\\n" "Stopping hdacd service on hdac ..."
  ansible-playbook -K maint_stop_hdac.yaml
  printf "%s\\n" "Stopping travis service on hdac ..."
  ansible-playbook -K maint_stop_cmt.yaml
  printf "%s\\n" "Stopping terra service on terra-full ..."
  ansible-playbook -K maint_stop_terra_full.yaml
  printf "%s\\n" "Stopping terra service on terra-lcd ..."
  ansible-playbook -K maint_stop_terra_lcd.yaml
  printf "%s\\n" "Stopping irisd service on irisnet-full ..."
  ansible-playbook maint_stop_irisnet_full.yaml
  printf "%s\\n" "Stopping irislcdX service on irisnet-lcd ..."
  ansible-playbook maint_stop_irisnet_lcd.yaml
  printf "%s\\n" "Stopping gaia-lite service on cosmoslcd ..."
  ansible-playbook maint_stop_cosmos_lcd.yaml

elif [ "$mode" = "check" ]; then
  printf "%s\\n" "Test stopping geth service on geth1 ..."
  ansible-playbook -K maint_stop_geth1.yaml --check
  printf "%s\\n" "Test stopping geth service on geth2 ..."
  ansible-playbook -K maint_stop_geth2.yaml --check
  printf "%s\\n" "Test stopping geth service on etc ..."
  ansible-playbook -K maint_stop_etc.yaml --check
  printf "%s\\n" "Test stopping hdacd service on hdac ..."
  ansible-playbook -K maint_stop_hdac.yaml --check
  printf "%s\\n" "Test stopping travis service on hdac ..."
  ansible-playbook -K maint_stop_cmt.yaml --check
  printf "%s\\n" "Test stopping terra service on terra-full ..."
  ansible-playbook -K maint_stop_terra_full.yaml --check
  printf "%s\\n" "Test stopping terra service on terra-lcd ..."
  ansible-playbook -K maint_stop_terra_lcd.yaml --check
  printf "%s\\n" "Test stopping wallet service on terra-lcd ..."
  ansible-playbook -K maint_stop_wallet.yaml --check
  printf "%s\\n" "Stopping irisd service on irisnet-full ..."
  ansible-playbook maint_stop_irisnet_full.yaml --check
  printf "%s\\n" "Stopping irislcdX service on irisnet-lcd ..."
  ansible-playbook maint_stop_irisnet_lcd.yaml --check
  printf "%s\\n" "Stopping gaia-lite service on cosmos-lcd ..."
  ansible-playbook maint_stop_cosmos_lcd.yaml --check

else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
