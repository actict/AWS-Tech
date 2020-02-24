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
  printf "%s\\n" "ansible2a execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_ansible2a.yaml


elif [ "$mode" = "check" ]; then
  printf "%s\\n" "Test ansible2a execute ..."
  ansible-playbook -K -i hosts_isms isms_diagnosis_ansible2a.yaml --check
else
  printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
