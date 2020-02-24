#!/usr/bin/env bash
# collectd_cw_post_setup_ubuntu_internal_api.sh
#
# Last Updated: 2018.09.10
# Updated by: hulk.choi@actwo.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "internal-api-svr" running Ubuntu 18.04
# with systemd (not upstart).

coldconf="/etc/collectd/collectd.conf"
whitelist="/opt/collectd-plugins/cloudwatch/config/whitelist.conf"

if [ "$USER" != "root" ]; then
  printf "%s\n" "### This script must be executed as root user! ###"
  exit 1
fi

### 1. Edit /etc/collectd.conf
# A. Enable collectd 'processes' plugin
printf "%s\n" "# Enabling 'processes' plugin"
sed -i 's:#LoadPlugin processes:LoadPlugin processes:g' "$coldconf"

# B. Define search strings for 'processes' plugin
printf "%s\n" "# Setting up regex for 'processes' plugin"
cat >> "$coldconf" <<EOF
<Plugin processes>
        ProcessMatch “java” "/usr/bin/java -jar -Dspring.profiles.active=production scouter.jar"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\n" "# Identify which collectd stats to send to Cloudwatch"

cat >> $whitelist <<EOF

processes.*
EOF


### 3. collectd setup for systemd
#rintf "%s\n" "# Enabling collectd at boot (systemctl)"
#ystemctl enable collectd
printf "%s\n" "# Restarting collectd daemon"
systemctl restart collectd
sleep 3
systemctl status collectd
