#!/usr/bin/env python3
# env_ami.py
#
# Last Updated: 2019.10.14
# Created by: joshua.huh@actwo.com
# Updated by: scott.hwang@peertec.com
#
# File containing AMI environment variables to be used in boto3
# scripts provisioning resources in all AWS accounts for Actwo 'PROD',
# 'DEV' etc.

### AMI Images ###
ami_amzn_linux2_gp2 = 'ami-0d097db2fb6e0f05e'  # hvm-2.0.20190823-x86_64-gp2
ami_ubuntu_1804 = 'ami-0df5bf8255e3a317f' # hvm:ebs-ssd 2019.10.10
ami_ubuntu_1604 = 'ami-030b841cf36fd3728' # hvm:ebs-ssd 2019.06.05
ami_wordpress = 'ami-3e115941' # Wordpress by Symetricore
