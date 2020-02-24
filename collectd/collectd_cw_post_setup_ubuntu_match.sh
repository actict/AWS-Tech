#!/usr/bin/env bash
# collectd_cw_post_setup_ubuntu_match.sh
#
# Last Updated: 2019.05.23
# Updated by: scott.hwang@peertec.com
#
# This script should be run after collectd and collectd
# Cloudwatch plugin have been installed. This script must
# be executed as root on "match" server running Ubuntu 16.04+
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
        ProcessMatch "match_ATOM-KRW" "match_no_th.py -p ATOM/KRW"
        ProcessMatch "trade_ATOM-KRW" "trade_receiver_v2.py -p ATOM/KRW"
        ProcessMatch "match_BCH-KRW" "match_no_th.py -p BCH/KRW"
        ProcessMatch "trade_BCH-KRW" "trade_receiver_v2.py -p BCH/KRW"
        ProcessMatch "match_BOS-GT" "match_no_th.py -p BOS/GT"
        ProcessMatch "trade_BOS-GT" "trade_receiver_v2.py -p BOS/GT"
        ProcessMatch "match_BOS-KRW" "match_no_th.py -p BOS/KRW"
        ProcessMatch "trade_BOS-KRW" "trade_receiver_v2.py -p BOS/KRW"
        ProcessMatch "match_BSV-KRW" "match_no_th.py -p BSV/KRW"
        ProcessMatch "trade_BSV-KRW" "trade_receiver_v2.py -p BSV/KRW"
        ProcessMatch "match_BTC-KRW" "match_no_th.py -p BTC/KRW"
        ProcessMatch "trade_BTC-KRW" "trade_receiver_v2.py -p BTC/KRW"
        ProcessMatch "match_CMT-KRW" "match_no_th.py -p CMT/KRW"
        ProcessMatch "trade_CMT-KRW" "trade_receiver_v2.py -p CMT/KRW"
        ProcessMatch "match_COSM-KRW" "match_no_th.py -p COSM/KRW"
        ProcessMatch "trade_COSM-KRW" "trade_receiver_v2.py -p COSM/KRW"
        ProcessMatch "match_DASH-KRW" "match_no_th.py -p DASH/KRW"
        ProcessMatch "trade_DASH-KRW" "trade_receiver_v2.py -p DASH/KRW"
        ProcessMatch "match_ENJ-GT" "match_no_th.py -p ENJ/GT"
        ProcessMatch "trade_ENJ-GT" "trade_receiver_v2.py -p ENJ/GT"
        ProcessMatch "match_ENJ-KRW" "match_no_th.py -p ENJ/KRW"
        ProcessMatch "trade_ENJ-KRW" "trade_receiver_v2.py -p ENJ/KRW"
        ProcessMatch "match_ETC-KRW" "match_no_th.py -p ETC/KRW"
        ProcessMatch "trade_ETC-KRW" "trade_receiver_v2.py -p ETC/KRW"
        ProcessMatch "match_ETH-GT" "match_no_th.py -p ETH/GT"
        ProcessMatch "trade_ETH-GT" "trade_receiver_v2.py -p ETH/GT"
        ProcessMatch "match_ETH-KRW" "match_no_th.py -p ETH/KRW"
        ProcessMatch "trade_ETH-KRW" "trade_receiver_v2.py -p ETH/KRW"
        ProcessMatch "match_GT-KRW" "match_no_th.py -p GT/KRW"
        ProcessMatch "trade_GT-KRW" "trade_receiver_v2.py -p GT/KRW"
        ProcessMatch "match_HDAC-GT" "match_no_th.py -p HDAC/GT"
        ProcessMatch "trade_HDAC-GT" "trade_receiver_v2.py -p HDAC/GT"
        ProcessMatch "match_HDAC-KRW" "match_no_th.py -p HDAC/KRW"
        ProcessMatch "trade_HDAC-KRW" "trade_receiver_v2.py -p HDAC/KRW"
        ProcessMatch "match_HOT-KRW" "match_no_th.py -p HOT/KRW"
        ProcessMatch "trade_HOT-KRW" "trade_receiver_v2.py -p HOT/KRW"
        ProcessMatch "match_IRIS-KRW" "match_no_th.py -p IRIS/KRW"
        ProcessMatch "trade_IRIS-KRW" "trade_receiver_v2.py -p IRIS/KRW"
        ProcessMatch "match_IRIS-BTC" "match_no_th.py -p IRIS/BTC"
        ProcessMatch "trade_IRIS-BTC" "trade_receiver_v2.py -p IRIS/BTC"
        ProcessMatch "match_LTC-KRW" "match_no_th.py -p LTC/KRW"
        ProcessMatch "trade_LTC-KRW" "trade_receiver_v2.py -p LTC/KRW"
        ProcessMatch "match_MITH-KRW" "match_no_th.py -p MITH/KRW"
        ProcessMatch "trade_MITH-KRW" "trade_receiver_v2.py -p MITH/KRW"
        ProcessMatch "match_OMG-KRW" "match_no_th.py -p OMG/KRW"
        ProcessMatch "trade_OMG-KRW" "trade_receiver_v2.py -p OMG/KRW"
        ProcessMatch "match_PCH-KRW" "match_no_th.py -p PCH/KRW"
        ProcessMatch "trade_PCH-KRW" "trade_receiver_v2.py -p PCH/KRW"
        ProcessMatch "match_RDN-KRW" "match_no_th.py -p RDN/KRW"
        ProcessMatch "trade_RDN-KRW" "trade_receiver_v2.py -p RDN/KRW"
        ProcessMatch "match_SNT-KRW" "match_no_th.py -p SNT/KRW"
        ProcessMatch "trade_SNT-KRW" "trade_receiver_v2.py -p SNT/KRW"
        ProcessMatch "match_UPP-KRW" "match_no_th.py -p UPP/KRW"
        ProcessMatch "trade_UPP-KRW" "trade_receiver_v2.py -p UPP/KRW"
        ProcessMatch "match_WGP-GT" "match_no_th.py -p WGP/GT"
        ProcessMatch "trade_WGP-GT" "trade_receiver_v2.py -p WGP/GT"
        ProcessMatch "match_WGP-KRW" "match_no_th.py -p WGP/KRW"
        ProcessMatch "trade_WGP-KRW" "trade_receiver_v2.py -p WGP/KRW"
        ProcessMatch "match_XLM-KRW" "match_no_th.py -p XLM/KRW"
        ProcessMatch "trade_XLM-KRW" "trade_receiver_v2.py -p XLM/KRW"
        ProcessMatch "match_XRP-GT" "match_no_th.py -p XRP/GT"
        ProcessMatch "trade_XRP-GT" "trade_receiver_v2.py -p XRP/GT"
        ProcessMatch "match_XRP-KRW" "match_no_th.py -p XRP/KRW"
        ProcessMatch "match_XRP-KRW" "match_no_th.py -p XRP/KRW"
        ProcessMatch "trade_XRP-KRW" "trade_receiver_v2.py -p XRP/KRW"
        ProcessMatch "match_ZEC-KRW" "match_no_th.py -p ZEC/KRW"
        ProcessMatch "trade_ZEC-KRW" "trade_receiver_v2.py -p ZEC/KRW"
        ProcessMatch "match_ZRX-KRW" "match_no_th.py -p ZRX/KRW"
        ProcessMatch "trade_ZRX-KRW" "trade_receiver_v2.py -p ZRX/KRW"
        ProcessMatch "cloudwatch" "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"
</Plugin>
EOF

# Note: as of 2018.08.13 there are 9 ccy pairs, so there will be
# 9 processes each for 'trade_receiver_v2.py' and 'match_no_th.py'

### 2. Edit /opt/collectd-plugins/cloudwatch/config/whitelist.conf
printf "%s\\n" "# Identify which collectd stats to send to Cloudwatch"

cat >> $whitelist <<EOF

df-var-log-match-percent_bytes-used
processes.*
EOF


### 3. collectd setup for systemd
#rintf "%s\n" "# Enabling collectd at boot (systemctl)"
#ystemctl enable collectd
printf "%s\\n" "# Restarting collectd daemon"
systemctl restart collectd
sleep 3
systemctl status collectd
