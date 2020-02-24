#!/usr/bin/env bash
# collectd_cw_post_setup_ubuntu_hdac.sh
#
# Last Updated: 2019.01.17
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd Cloudwatch
# plugin have been installed. This script must be executed as root on
# "hdac" running Ubuntu 18.04 with systemd (not upstart).

coldconf="/etc/collectd/collectd.conf"
whitelist="/opt/collectd-plugins/cloudwatch/config/whitelist.conf"

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
cat >> "$coldconf" <<EOF
<Plugin processes>
        ProcessMatch "hdac" "hdacd hdac@seed.as.hdactech.com:8823"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"

cat >> $whitelist <<EOF

df-home-hdac-.hdac-percent_bytes-used
processes.*
EOF


### 3. collectd setup for systemd
printf "%s\\n" "# Enabling collectd at boot (systemctl)"
systemctl enable collectd
printf "%s\\n" "# Restarting collectd daemon"
systemctl restart collectd
sleep 3
systemctl status collectd
