#!/usr/bin/env python3\

"""
env_candy.py

Last Updated: 2018.11.26
Updated by: joshua.huh@actwo.com

File containing environment variables to be used in boto3
scripts provisioning resources in the AWS 'candy' account.
Refer to https://cloud-images.ubuntu.com/locator/ec2/
to search for latest Ubuntu AMI IDs
"""

ami_ubuntu_1804 = 'ami-0a5eaf03968d0f65c'  # hvm:ebs-ssd, released 2018.11.05
ami_ubuntu_1604 = 'ami-0eee4dcc71fced4cf'  # hvm:ebs-ssd, released 2018.11.14
ami_amazon_linux2 = 'ami-0b4fdb56a00adb616'  # hvm:gp2, released 2018.11.14
subnet_dmz = 'subnet-0deb4ee540fec7047'
# iam_profile = '' # this line is used for collectd monitoring
sg_candy_beanstalk = 'sg-0c0c49388d7a9f0b7'
sg_candy_deploy_group = 'sg-0954a742a11b1dcd0'
sg_candy_sandbox_candy_crawler = 'sg-0b2c21dab1dd450ba'
sg_candy_candy_control = 'sg-0032b4d1b1b5311f0'

ssh_candy = 'doncandy-seoul'