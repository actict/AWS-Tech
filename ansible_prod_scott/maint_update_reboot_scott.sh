#!/bin/bash
# maint_update_reboot.sh
#
# Last Updated: 2019.08.13
# Updated by: scott.hwang@actwo.com
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
  printf "%s\\n" "Updating pkgs on gl-batch-0 ..."
  ansible-playbook maint_update_gl_batch_0.yaml
  printf "%s\\n" "Updating pkgs on gl-batch-1 ..."
  ansible-playbook maint_update_gl_batch_1.yaml
  printf "%s\\n" "Updating pkgs on gl-batch2 ..."
  ansible-playbook maint_update_gl_batch_2.yaml
  printf "%s\\n" "Updating pkgs on pl-batch ..."
  ansible-playbook maint_update_pl_batch.yaml
  printf "%s\\n" "Updating pkgs on cruiser ..."
  ansible-playbook maint_update_cruiser.yaml
  printf "%s\\n" "Updating pkgs on ledger ..."
  ansible-playbook maint_update_ledger.yaml
  printf "%s\\n" "Updating pkgs on match ..."
  ansible-playbook maint_update_match.yaml
  printf "%s\\n" "Updating pkgs on peer-mysql ..."
  ansible-playbook maint_update_peer_mysql.yaml
  printf "%s\\n" "Updating pkgs on blockinpress-web ..."
  ansible-playbook maint_update_blockinpress_web.yaml
  printf "%s\\n" "Updating pkgs on kakaopay ..."
  ansible-playbook maint_update_kakaopay.yaml
  printf "%s\\n" "Updating pkgs on internal-api ..."
  ansible-playbook maint_update_internal_api.yaml
  printf "%s\\n" "Updating pkgs on logger ..."
  ansible-playbook maint_update_logger.yaml
  printf "%s\\n" "Updating pkgs on peertec ..."
  ansible-playbook maint_update_peertec.yaml
  printf "%s\\n" "Updating pkgs on deconomy ..."
  ansible-playbook maint_update_deconomy.yaml
  printf "%s\\n" "Updating pkgs on hashtower ..."
  ansible-playbook maint_update_hashtower.yaml
  printf "%s\\n" "Updating pkgs on certmanager ..."
  ansible-playbook maint_update_certmanager.yaml
  printf "%s\\n" "Updating pkgs on front-1 ..."
  ansible-playbook maint_update_front_1.yaml
  printf "%s\\n" "Updating pkgs on front-2 ..."
  ansible-playbook maint_update_front_2.yaml
  printf "%s\\n" "Updating pkgs on service-admin ..."
  ansible-playbook maint_update_service_admin.yaml
  printf "%s\\n" "Updating pkgs on admin ..."
  ansible-playbook maint_update_admin.yaml
  printf "%s\\n" "Updating pkgs on jenkins ..."
  ansible-playbook maint_update_jenkins.yaml
  printf "%s\\n" "Updating pkgs on front-alpha ..."
  ansible-playbook maint_update_front_alpha.yaml
  printf "%s\\n" "Updating pkgs on front-beta ..."
  ansible-playbook maint_update_front_beta.yaml
  printf "%s\\n" "Updating pkgs on bitgo-webhook ..."
  ansible-playbook maint_update_bitgo_webhook.yaml
  printf "%s\\n" "Updating pkgs on bitgo-api ..."
  ansible-playbook maint_update_bitgo-api.yaml

elif [ "$mode" = "check" ]; then
  printf "%s\\n" "Updating pkgs on gl-batch-0 ..."
  ansible-playbook maint_update_gl_batch_0.yaml --check
  printf "%s\\n" "Updating pkgs on gl-batch-1 ..."
  ansible-playbook maint_update_gl_batch_1.yaml --check
  printf "%s\\n" "Updating pkgs on gl-batch2 ..."
  ansible-playbook maint_update_gl_batch_2.yaml --check
  printf "%s\\n" "Updating pkgs on pl-batch ..."
  ansible-playbook maint_update_pl_batch.yaml --check
  printf "%s\\n" "Updating pkgs on cruiser ..."
  ansible-playbook maint_update_cruiser.yaml --check
  printf "%s\\n" "Updating pkgs on ledger ..."
  ansible-playbook maint_update_ledger.yaml --check
  printf "%s\\n" "Updating pkgs on match ..."
  ansible-playbook maint_update_match.yaml --check
  printf "%s\\n" "Updating pkgs on peer-mysql ..."
  ansible-playbook maint_update_peer_mysql.yaml --check
  printf "%s\\n" "Updating pkgs on blockinpress-web ..."
  ansible-playbook maint_update_blockinpress_web.yaml --check
  printf "%s\\n" "Updating pkgs on kakaopay ..."
  ansible-playbook maint_update_kakaopay.yaml --check
  printf "%s\\n" "Updating pkgs on internal-api ..."
  ansible-playbook maint_update_internal_api.yaml --check
  printf "%s\\n" "Updating pkgs on logger ..."
  ansible-playbook maint_update_logger.yaml --check
  printf "%s\\n" "Updating pkgs on peertec ..."
  ansible-playbook maint_update_peertec.yaml --check
  printf "%s\\n" "Updating pkgs on deconomy ..."
  ansible-playbook maint_update_deconomy.yaml --check
  printf "%s\\n" "Updating pkgs on hashtower ..."
  ansible-playbook maint_update_hashtower.yaml --check
  printf "%s\\n" "Updating pkgs on certmanager ..."
  ansible-playbook maint_update_certmanager.yaml --check
  printf "%s\\n" "Updating pkgs on front-1 ..."
  ansible-playbook maint_update_front_1.yaml --check
  printf "%s\\n" "Updating pkgs on front-2 ..."
  ansible-playbook maint_update_front_2.yaml --check
  printf "%s\\n" "Updating pkgs on service-admin ..."
  ansible-playbook maint_update_service_admin.yaml --check
  printf "%s\\n" "Updating pkgs on admin ..."
  ansible-playbook maint_update_admin.yaml --check
  printf "%s\\n" "Updating pkgs on jenkins ..."
  ansible-playbook maint_update_jenkins.yaml --check
  printf "%s\\n" "Updating pkgs on front-alpha ..."
  ansible-playbook maint_update_front_alpha.yaml --check
  printf "%s\\n" "Updating pkgs on front-beta ..."
  ansible-playbook maint_update_front_beta.yaml --check
  printf "%s\\n" "Updating pkgs on bitgo-webhook ..."
  ansible-playbook maint_update_bitgo_webhook.yaml --check
  printf "%s\\n" "Updating pkgs on bitgo-api ..."
  ansible-playbook maint_update_bitgo-api.yaml --check


else
    printf "%s\\n" "Invalid mode! Choose one of 'check' or 'real'!"
  exit 1
fi
