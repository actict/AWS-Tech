#!/usr/bin/env bash
# setup_cw_collectd_deb.sh
#
# Last Updated: 2019.01.17
# Updated by: scott.hwang@peertec.com
#
# This script installs collectd and the collectd plugin for
# AWS Cloudwatch on Ubuntu 16.04+. The appropriate IAM role must
# be applied to the EC2 instance this script will run on. This script
# requires an Internet connection to wget the CW plugin from Github
# and for getting packages with apt-get. This script must be run
# as ROOT.


printf "%s\\n" "### Checking Internet Connection ###"
if curl -s http://google.com; then
  :
else
  printf "%s\\n" "### No Internet Connection! Exiting... ###"
  exit 1
fi

# Install collectd pkgs w/o X11 GUI deps
apt update; apt install -y collectd-core
apt install -y --no-install-recommends collectd

# Download collectd-cloudwatch plugin, make executable
wget -N https://raw.githubusercontent.com/awslabs/collectd-cloudwatch/master/src/setup.py \
     -O /root/setup.py
chmod +x /root/setup.py

# Edit setup.py to use python2 instead of just 'python'
if ! (head -n 1 /root/setup.py | grep python2); then
  sed -i 's:/usr/bin/env python:/usr/bin/env python2:g' setup.py
  # Note: on Ubuntu 18.04.1 you have to use 'python2.7' instead
  # of just 'python2'
fi

# Run setup.py in non-interactive mode
/root/setup.py --non_interactive --enable_high_resolution_metrics \
               --installation_method recommended
