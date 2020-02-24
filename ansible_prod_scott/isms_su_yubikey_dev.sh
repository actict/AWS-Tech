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
  printf "%s\\n" "klay-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaydev.yaml
  printf "%s\\n" "klay-devmain execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaydevmain.yaml
  printf "%s\\n" "etc-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_etcdev.yaml
  printf "%s\\n" "cmt-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cmtdev.yaml
  printf "%s\\n" "geth-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_gethdev.yaml
  printf "%s\\n" "hdac-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hdacdev.yaml
  printf "%s\\n" "terra-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terradev.yaml
  printf "%s\\n" "terra-devmain execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terradevmain.yaml
  printf "%s\\n" "dev-priv execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_devpriv.yaml


elif [ "$mode" = "check" ]; then
  printf "%s\\n" "Test klay-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaydev.yaml --check
  printf "%s\\n" "Test klay-devmain execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_klaydevmain.yaml --check
  printf "%s\\n" "Test etc-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_etcdev.yaml --check
  printf "%s\\n" "Test cmt-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_cmtdev.yaml --check
  printf "%s\\n" "Test geth-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_gethdev.yaml --check
  printf "%s\\n" "Test hdac-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_hdacdev.yaml --check
  printf "%s\\n" "Test terra-dev execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terradev.yaml --check
  printf "%s\\n" "Test terra-devmain execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_terradevmain.yaml --check
  printf "%s\\n" "Test dev-priv execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_devpriv.yaml --check
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
