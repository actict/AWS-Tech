#!/usr/bin/env bash
# collectd_cw_post_setup_ubuntu_cruiser.sh
#
# Last Updated: 2019.03.06
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "bip-*" servers running Ubuntu 16.04+
# with systemd (not upstart).


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
        ProcessMatch "cruiser" "cruiser.jar"
</Plugin>
EOF

### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"


cat >> $whitelist <<EOF

processes.*
EOF
