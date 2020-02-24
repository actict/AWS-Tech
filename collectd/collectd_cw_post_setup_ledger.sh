#!/usr/bin/env bash
# collectd_post_setup_amzn_linux2_ledger-tonghap.sh
#
# Last Updated: 2019.05.23
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "ledger-tonghap" running Amazon Linux 2
# with systemd (not upstart).


whitelist="/opt/collectd-plugins/cloudwatch/config/whitelist.conf"

if [ "$USER" != "root" ]; then
  printf "%s\\n" "### This script must be executed as root user! ###"
  exit 1
fi

### 1. Edit /etc/collectd.conf
# A. Enable collectd 'processes' plugin
printf "%s\\n" "# Enabling 'processes' plugin"
sed -i 's:#LoadPlugin processes:LoadPlugin processes:g' /etc/collectd.conf

# B. Define search strings for 'processes' plugin
printf "%s\\n" "# Setting up regex for 'processes' plugin"
cat >> /etc/collectd.conf <<EOF
<Plugin processes>
        ProcessMatch "PM2" "God Daemon"
        ProcessMatch "admin" "node /home/ec2-user/ledger-admin/source/src/index.js"
        ProcessMatch "db2w" "node /home/ec2-user/new-ledger-db2w/source/src/index.js"
        ProcessMatch "dcq" "node /home/ec2-user/ledger-dcq/source/src/index.js"
        ProcessMatch "notification" "node /home/ec2-user/ledger-notification/source/src/index.js"
        ProcessMatch "otp" "app_otp.js"
        ProcessMatch "w2db" "node /home/ec2-user/ledger-w2db/source/src/index.js"
        ProcessMatch "msg_sender" "peer_msg_sender.py"
        ProcessMatch "req_router" "wd_req_router.py"
        ProcessMatch "proc" "wd_proc.py"
        ProcessMatch "cloudwatch" "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"

cat >> $whitelist <<EOF

processes.*
EOF


### 3. collectd setup for chkconfig and upstart
printf "%s\\n" "# Enabling collectd at boot (systemctl)"
systemctl enable collectd
printf "%s\\n" "# Starting collectd daemon"
systemctl start collectd
systemctl status collectd
