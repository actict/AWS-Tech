#!/usr/bin/env bash
# collectd_post_setup_amzn_linux2_front.sh
#
# Last Updated: 2018.07.09
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "front" running Amazon Linux 2
# with systemd (not upstart).


whitelist="/opt/collectd-plugins/cloudwatch/config/whitelist.conf"

if [ "$USER" != "root" ]; then
  printf "%s\n" "### This script must be executed as root user! ###"
  exit 1
fi

### 1. Edit /etc/collectd.conf
# A. Enable collectd 'processes' plugin
printf "%s\n" "# Enabling 'processes' plugin"
sed -i 's:#LoadPlugin processes:LoadPlugin processes:g' /etc/collectd.conf

# B. Define search strings for 'processes' plugin
printf "%s\n" "# Setting up regex for 'processes' plugin"
cat >> /etc/collectd.conf <<EOF
<Plugin processes>
        ProcessMatch "nginx" "nginx: master process"
        ProcessMatch "PM2" "God Daemon"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\n" "# Identify which collectd stats to send to Cloudwatch"

cat >> $whitelist <<EOF

processes.*
EOF


### 3. collectd setup for chkconfig and upstart
printf "%s\n" "# Enabling collectd at boot (systemctl)"
systemctl enable collectd
printf "%s\n" "# Starting collectd daemon"
systemctl start collectd
systemctl status collectd
