#!/usr/bin/env bash
# setup_cw_collectd_rpm.sh
#
# Last Updated: 2018.06.07
# Updated by: scott.hwang@peertec.com
#
# This script installs collectd and the collectd plugin for
# AWS Cloudwatch on RH-based distros. The appropriate IAM role must
# be applied to the EC2 instance this script will run on. This script
# requires an Internet connection to wget the CW plugin from Github
# and for getting packages with apt-get. This script must be run
# as ROOT.

printf "%s\n" "### Checking Internet Connection ###"
if curl -s http://google.com; then
  :
else
  printf "%s\n" "### No Internet Connection! Exiting... ###"
  exit 1
fi

yum install -y collectd collectd-python

# Download collectd-cloudwatch plugin, make executable
wget https://raw.githubusercontent.com/awslabs/collectd-cloudwatch/master/src/setup.py
chmod +x setup.py

# check if 'python27' pkg installed
if rpm -q python27; then
  :
else
  printf "%s\n" "### You must install python2.7 to run setup.py ###"
  exit 1
fi

# When setup.py is executed, it requires user input; this automation
# will be done later with "expect", if at all
#setup.py
