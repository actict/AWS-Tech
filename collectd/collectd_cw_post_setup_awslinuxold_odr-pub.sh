#!/usr/bin/env bash
# collectd_cw_post_setup_awslinuxold_ord-pub.sh
#
# Last Updated: 2019.03.20
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on David's EB odr-pub running
# an old version of Amazon Linux < v2 using upstart init
# (not systemd).


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
        ProcessMatch "nginx" "/usr/sbin/nginx"
        ProcessMatch "appordbookpub" "node appOrdBookPub.js"
        ProcessMatch "cloudwatch" "/usr/bin/aws logs push"
</Plugin>
EOF


### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"


cat >> $whitelist <<EOF

processes.*
EOF



### 3. collectd setup for chkconfig and upstart
printf "%s\\n" "# Enabling collectd to start at boot (chkconfig)"
chkconfig --level 2345 collectd on
printf "%s\\n" "# Starting collectd daemon"
service collectd restart
service collectd status
