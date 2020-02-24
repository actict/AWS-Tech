#!/usr/bin/env bash
# setup_cw_collectd_rpm_amzn_linux2.sh
#
# Last Updated: 2018.07.02
# Updated by: scott.hwang@peertec.com
#
# This script installs collectd and the collectd plugin for AWS
# Cloudwatch on Amazon Linux v2.0+. The appropriate IAM role must be
# applied to the EC2 instance this script will run on. This script
# requires an Internet connection to wget the CW plugin from Github
# and for getting packages with apt-get. This script must be run as
# ROOT.


if [ "$USER" != "root" ]; then
  printf "%s\n" "### This script must be executed as root user! ###"
  exit 1
fi

printf "%s\n" "### Checking Internet Connection ###"
if curl -s http://google.com; then
  :
else
  printf "%s\n" "### No Internet Connection! Exiting... ###"
  exit 1
fi

wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -P /tmp
yum install -y /tmp/epel-release-latest-7.noarch.rpm
yum install -y collectd

# Download collectd-cloudwatch plugin, make executable
wget https://raw.githubusercontent.com/awslabs/collectd-cloudwatch/master/src/setup.py
chmod +x setup.py

# check if 'python27' pkg installed
if rpm -q python; then
  :
else
  printf "%s\n" "### You must install python2.7 to run setup.py ###"
  exit 1
fi

printf "%s\n" "### Edit setup.py to run on Amazon Linux 2 ###"
sed -i 's:Amazon Linux AMI:Amazon Linux:g' setup.py

# When setup.py is executed, it requires user input; this automation
# will be done later with "expect", if at all
#setup.py
