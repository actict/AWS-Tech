#!/bin/bash
# isms_su.sh
#
# Last Updated: 2020.02.19
# Updated by: scott.hwang@peertec.com

mode="$1"

if [ $# -ne 1 ]; then
  printf "%s\\n" "### Please specify mode: 'check' or 'real'! ###"
  exit 1
fi


if [ "$mode" = "real" ]; then
  printf "%s\\n" "bitgo-webhook execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_bitgo-webhook.yaml
  printf "%s\\n" "bitgo-api execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_bitgo-api.yaml
  printf "%s\\n" "hvault execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hvault.yaml
  printf "%s\\n" "terra-full execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terra-full.yaml
  printf "%s\\n" "terra-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terra-lcd.yaml
  printf "%s\\n" "wallet execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_wallet.yaml
  printf "%s\\n" "cmt execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cmt.yaml
  printf "%s\\n" "cosmos-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cosmos-lcd.yaml
  printf "%s\\n" "etc execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_etc.yaml
  printf "%s\\n" "geth1 execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_geth1.yaml
  printf "%s\\n" "geth2 execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_geth2.yaml
  printf "%s\\n" "hdac execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hdac.yaml
  printf "%s\\n" "klaytn execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaytn.yaml
  printf "%s\\n" "genesis execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_genesis.yaml
  printf "%s\\n" "irisnet-full execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_irisnet-full.yaml
  printf "%s\\n" " irisnet-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_irisnet-lcd.yaml


elif [ "$mode" = "check" ]; then
  printf "%s\\n" "Test bitgo-webhook execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_bitgo-webhook.yaml --check
  printf "%s\\n" "Test bitgo-api execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_bitgo-api.yaml --check
  printf "%s\\n" "Test hvault execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hvault.yaml --check
  printf "%s\\n" "Test terra-full execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terra-full.yaml --check
  printf "%s\\n" "Test terra-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terra-lcd.yaml --check
  printf "%s\\n" "Test wallet execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_wallet.yaml --check
  printf "%s\\n" "Test cmt execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cmt.yaml --check
  printf "%s\\n" "Test cosmos-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cosmos-lcd.yaml --check
  printf "%s\\n" "Test etc execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_etc.yaml --check
  printf "%s\\n" "Test geth1 execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_geth1.yaml --check
  printf "%s\\n" "Test geth2 execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_geth2.yaml --check
  printf "%s\\n" "Test hdac execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hdac.yaml --check
  printf "%s\\n" "Test klaytn execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaytn.yaml --check
  printf "%s\\n" "Test genesis execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_genesis.yaml --check
  printf "%s\\n" "Test irisnet-full execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_irisnet-full.yaml --check
  printf "%s\\n" "Test irisnet-lcd execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_irisnet-lcd.yaml --check
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
