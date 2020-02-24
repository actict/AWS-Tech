#!/usr/bin/env bash
# collectd_cw_post_setup_ubuntu_blockinpress.sh
#
# Last Updated: 2018.12.28
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "bip-*" servers running Ubuntu 18.04
# with systemd (not upstart).

# TODO: if stmt writing different collectd 'processes'
# configs does not work! Need to debug or create separate
# collectd post-setup scripts for bip-web and bip-mysql...

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

if pgrep mysqld &>/dev/null; then
cat >> "$coldconf" <<EOF
<Plugin processes>
        ProcessMatch "mysql" "/usr/sbin/mysqld --daemonize"
</Plugin>
EOF
fi

if pgrep apache2 &>/dev/null; then
cat >> "$coldconf" <<EOF
<Plugin processes>
        ProcessMatch "apache2" "/usr/sbin/apache2 -k start"
</Plugin>
EOF
fi


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"

if pgrep mysqld &>/dev/null; then
cat >> $whitelist <<EOF

df-var-lib-mysql-percent_bytes-used
processes.*
EOF
fi

if pgrep apache2 &>/dev/null; then
cat >> $whitelist <<EOF

df-var-www-html-percent_bytes-used
processes.*
EOF
fi
