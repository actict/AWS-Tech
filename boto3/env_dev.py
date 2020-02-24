#!/usr/bin/env python3
# env_dev.py
#
# Last Updated: 2019.10.14
# Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com, scott.hwang@actwo.com
#
# File containing environment variables to be used in boto3 scripts
# provisioning resources in the AWS 'DEV' account.

### AWS Account IDs ###

aws_id_dict = {
    'prod' : '762015387773',
    'dev' : '905136931838'
}

### VPCs ###

vpc_dict = {
    # 172.29.0.0/16
    'mainnet' : 'vpc-0dfeb1ed0a78c97f0',
    # # 172.31.0.0/16
    'testnet' : 'vpc-22d8504a'
}

dev_mainnet = 'vpc-0dfeb1ed0a78c97f0' # 172.29.0.0/16
dev_testnet = 'vpc-22d8504a' # 172.31.0.0/16

### Subnets ###

subnet_dict = {
    # dev-mainnet private 2a 172.29.0.0/16
    'private-2a' : 'subnet-00f288f9dba557932',
    # dev-mainnet private 2c 172.29.1.0/24
    'private-2c' : 'subnet-00f288f9dba557932',
    # dev-mainnet public 2a 172.29.254.0/24
    'public-2a' : 'subnet-06739379b072cd86e',
    # dev-mainnet public 2c 172.29 .255.0/24
    'public-2c' : 'subnet-0c388d0c898bcfbc7',
    # dev-testnet 2a 172.31.0.0/20
    'testnet-2a' : 'subnet-cfb5d0a7',
    # dev-testnet 2c 172.31.16.0/20
    'testnet-2c' : 'subnet-1ef23852',
    #dev-testnet 172.31.32.0/24
    'testnet-lb-2a' : 'subnet-0b8924a0ad0fde103',
    #dev-testnet 172.31.33.0/24
    'testnet-lb-2c' : 'subnet-0151ae36be2ddecb7'
}

subnet_pri_2a = 'subnet-00f288f9dba557932' # dev-mainnet 172.29.0.0/16
subnet_pri_2c = 'subnet-05d5695144f0484bf' # dev-mainnet 172.29.1.0/24
subnet_pub_2a = 'subnet-06739379b072cd86e' # dev-mainnet 172.29.254.0/24
subnet_pub_2c = 'subnet-0c388d0c898bcfbc7' # dev-mainnet 172.29.255.0/24
subnet_testnet_2a = 'subnet-cfb5d0a7' # dev-testnet 172.31.0.0/20
subnet_testnet_2c = 'subnet-1ef23852' # dev-testnet 172.31.16.0/20
subnet_lb_internal_2a = 'subnet-0b8924a0ad0fde103' #dev-testnet 172.31.32.0/24
subnet_lb_internal_2c = 'subnet-0151ae36be2ddecb7' #dev-testnet 172.31.33.0/24


### IAM Profiles ###
iam_profile_dict = {
    'collectd' : 'arn:aws:iam::905136931838:instance-profile/phoenix-cw-collectd-dev',
    'ec2-for-eb' : 'arn:aws:iam::905136931838:role/aws-elasticbeanstalk-ec2-role'
}


### Security Groups ###
sec_group_dict = {
    'auth-bank-dev' : 'sg-0689e586e5ad69f3c',
    'cosmos' : 'sg-03d94c429db4515ee',
    'cosmos-lcd' : 'sg-0a4fb7180b9cac5ed',
    'cosmos-wallet' : 'sg-07100f6448d525127',
    'exchange-fx' : 'sg-0870f8bba02b270e5',
    'grow-dev' : 'sg-0e274b1f6131bd987',
    'hashivault' : 'sg-0cce61dff526b6e59',
    'pay-orderbot' : 'sg-055ea7344e8326c2b',
    'sauron' : 'sg-0c687741240a500a1',
    'sky' : 'sg-053c2fe34073f889d',
    'sky-lb' : 'sg-07157172116f2848c',
    'wireguard-ng' : 'sg-006b015b9ef420f49',
    'wireguard-ng-testnet' : 'sg-061bcb052e0bd990d',
    'wireguard-ssh' : 'sg-063d1fb1080d6a9ab'
}


### SSH Keys ###
ssh_keys_dict = {
    'connector' : 'connector',
    'exchange-fx' : 'exchange-fx',
    'grow' : 'grow',
    'pay-orderbot' : 'pay-orderbot',
    'private' : 'dev-real-private-20180627c',
    'sauron' : 'sauron',
    'sky' : 'sky',
    'james-dev' : 'james-dev'
}


### EC2 InstanceId's mapped to Human-Readable Names
iid_wg_dev = 'i-0f99a6f91ab20bd24'


### Amazon Resource Numbers for SNS Topics
sns_wireguard_dev = 'arn:aws:sns:ap-northeast-2:905136931838:wireguard-dev'

### CIDR IP List
# Candyshop
cidr_candy_deploy = '13.209.222.12/32'
cidr_candy_halls = '13.209.253.236/32'
cidr_candy_halls_2 = '52.78.3.173/32'
cidr_candy_ricola = '13.124.182.139/32'
cidr_sandbox_candy_app = '13.125.103.201/32'
cidr_sandbox_candy_db_redis = '13.209.227.148/32'

# prod
cidr_any = '0.0.0.0/0'
cidr_nat_gw_2a = '13.124.216.13/32'
cidr_nat_gw_2c = '13.125.143.33/32'
cidr_nat_gw_dmz = '13.125.157.3/32'
cidr_zia_office = '114.203.208.0/24'
