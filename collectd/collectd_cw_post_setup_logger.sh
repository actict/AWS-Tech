#!/usr/bin/env bash
# collectd_cw_post_setup_logger.sh
#
# Last Updated: 2019.09.15
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "logstash" server running on
# Amazon Linux 2 with systemd. This script is intended
# to be executed by Ansible.


whitelist="/opt/collectd-plugins/cloudwatch/config/whitelist.conf"
coldconf="/etc/collectd.conf"


if [ "$USER" != "root" ]; then
  printf "%s\\n" "### This script must be executed as root user! ###"
  exit 1
fi

### 1. Edit /etc/collectd.conf
# A. Enable collectd 'processes' plugin
printf "%s\\n" "# Enabling 'processes' plugin"
sed -i 's:#LoadPlugin processes:LoadPlugin processes:g' "$coldconf"

# B. Define search strings for 'processes' plugin
printf "%s\\n" "# Setting up regex for 'processes' plugin"
cat >> $coldconf <<EOF
<Plugin processes>
        ProcessMatch "cloudwatch" "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"


cat >> $whitelist <<EOF

processes.*
EOF


### 3. collectd setup for systemd
printf "%s\\n" "# Enabling collectd at boot (systemd)"
systemctl enable collectd
printf "%s\\n" "# Starting collectd daemon"
systemctl start collectd
sleep 1
systemctl status collectd
