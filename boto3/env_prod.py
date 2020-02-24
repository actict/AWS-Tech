#!/usr/bin/env python3
# env_prod.py
#
# Last Updated: 2019.10.22
# Updated by: joshua.huh@actwo.com, scott.hwang@peertec.com, scott.hwang@actwo.com
#
# File containing environment variables to be used in boto3 scripts
# provisioning resources in the AWS 'PROD' account.


''' Private IP address blocks
PRIVATE NETWORK ADDRESS SHOULD BE DEFINED WITHIN THE PRIVATE
ADDRESS NETWORK BLOCK!!!
    10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
        10.0.0.0/16: GDAC VPC
            10.0.54.0/24 not assigned
            10.0.55.0/24 not assigned
            10.0.58.0/24 ~ 10.0.93.0/24 not assigned
            10.0.104.0/24 ~ 10.0.219.0/24 not assigned
            10.0.240.0/24 ~ 10.0.251.0/24 not assigned
    172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
        172.16.0.0/16: GCP validator network
            172.16.76.0/24: cmt-internal
            172.16.77.0/24: cmt-external
            172.16.78.0/24: cosmos-mainnet-internal
            172.16.79.0/24: cosmos-mainnet-external
        172.17.0.0/16: PEER VPC
            172.17.0.0/24: bip-public-2a
            172.17.1.0/24: bip-public-2c
            172.17.128.0/24: bip-private-2a
            172.17.129.0/24: bip-private-2c
            172.17.2.0/24: peer-pub-2a
            172.17.3.0/24: peer-pub-2c
            172.17.4.0/23: peer-pri-2a
            172.17.6.0/23: peer-pri-2c
        172.19.0.0/24 - 172.19.5.0/24: Actwo Office
            172.19.0.0/24: 사무실 인프라
            172.19.1.0/24: 개발 서버망
            172.19.2.0/24: Actwo (개발 외)
            172.19.3.0/24: Actgwo (개발)
            172.19.4.0/24: Reserved
            172.19.5.0/24: BIP
        172.29.0.0/16: DEV VPC, dev-mainnet
            172.29.0.0/24: private-2a
            172.29.1.0/24: private-2c
            172.29.254.0/24: public-2a
            172.29.255.0/24: public-2c
        172.31.0.0/16: DEV VPC, dev-testnet
            172.31.0.0/20: testnet-2a
            172.31.16.0/20: testnet-2c
            172.31.32.0/24: testnet-lb-internal-2a
            172.31.33.0/24: testnet-lb-internal-2a
    192.168.0.0/16 (192.168.0.0 - 192.168.255.255): PRIMARILY OCCUPIED BY PECUNIAN VPC
        192.168.0.0/24: candyshop
        192.168.111.0/24: GDAC wireguard virtual network
        192.168.112.0/24: PEER wireguard virtual network
        192.168.113.0/24: DEV wireguard virtual network
        192.168.114.0/24: CANDY wireguard virtual network
        192.168.117.0/24: GATE wireguard virtual network
        192.168.210.0/24: FLETA GCP external subnet
        192.168.211.0/24: FLETA GCP internal subnet
'''

### AWS Account IDs ###

aws_id_dict = {
    'prod' : '762015387773',
    'dev' : '905136931838'
}

vpc_dict = {
    'gdac' : 'vpc-05c9072df6997bec2',
    'peer' : 'vpc-0f14a6b9e225b5015'
}


subnet_dict = {
    # 10.0.0.0/22 nat
    'dmz-access-2a' : 'subnet-08f7599b33ffd0d0d',
    # 10.0.16.0/2 nat
    'dmz-access-2c' : 'subnet-0d9683d119d7f2d07',
    # 10.0.220.0/2 igw
    'dmz-access-lb-2a' : 'subnet-006bb17815931274a',
    # 10.0.221.0/2 igw
    'dmz-access-lb-2c' : 'subnet-0d9683d119d7f2d07',
    # 10.0.100.0/24
    'dmz-api-eb-2a' : 'subnet-0d133d6c11c40932b',
    # 10.0.101.0/24
    'dmz-api-eb-2c' : 'subnet-01da4b45353ef8482',
    # 10.0.102.0/24
    'dmz-api-ec2-2a' : 'subnet-0375d75f1ff47d23f',
    # 10.0.103.0/24
    'dmz-api-ec2-2c' : 'subnet-04dbe7ae09ff4501b',
    # 10.0.32.0/2 igw
    'dmz-auth-kakao-2a' : 'subnet-0457d81a7a6d13bba',
    # 10.0.33.0/2 igw
    'dmz-auth-kakao-2c' : 'subnet-0b4431ef7f8346538',
    # 10.0.236.0/2 igw
    'dmz-auth-kakao-lb-2a' : 'subnet-0487def63a54de9fe',
    # 10.0.237.0/2 igw
    'dmz-auth-kakao-lb-2c' : 'subnet-08c57709704cbebdf',
    # 10.0.96.0/24 igw
    'dmz-lb-2a' : 'subnet-0312e9d5395a788e7',
    # 10.0.97.0/24 igw
    'dmz-lb-2c' : 'subnet-0ed0fc7d76f3ae544',
    # 10.0.254.0/24 igw
    'dmz-mgmt-2a' : 'subnet-0fea3d7e77bde6b89',
    # 10.0.255.0/24 igw
    'dmz-mgmt-2c' : 'subnet-03dc74cf4d1d63118',
    # 10.0.98.0/24 igw
    'dmz-misc-2a' : 'subnet-015012d8f1bf85229',
    # 10.0.99.0/24 igw
    'dmz-misc-2c' : 'subnet-05333be2d87754d06',
    # 10.0.36.0/24, nat
    'dmz-noti-2a' : 'subnet-028da959b7d0f6137',
    # 10.0.37.0/24, nat
    'dmz-noti-2c' : 'subnet-0bc3a0af339b82910',
    # 10.0.222.0/24, nat
    'dmz-noti-lb-2a' : 'subnet-0c9aee37f760bea1f',
    # 10.0.223.0/24, nat
    'dmz-noti-lb-2c' : 'subnet-08150fcb736bad6d2',
    # 10.0.34.0/24, nat
    'dmz-wallet-2a' : 'subnet-0501058e2ca39a343',
    # 10.0.35.0/24, nat
    'dmz-wallet-2c' : 'subnet-0180fdd1619701c02',
    # 10.0.238.0/24, igw
    'nat-2a' : 'subnet-0f9ea87a3f6d76d78',
    # 10.0.239.0/24, igw
    'nat-2c' : 'subnet-0cab8f0ff15beff10',
    # 10.0.46.0/24
    'admin-2a' : 'subnet-0b2f1492be7d41e40',
    # 10.0.47.0/24
    'admin-2c' : 'subnet-0ad96441a8b52a42a',
    # 10.0.56.0/24
    'auroradb-2a' : 'subnet-025501a9fa5f5b334',
    # 10.0.57.0/42
    'auroradb-2c' : 'subnet-08a761d7e164d51ba',
    # 10.0.230.0/24 -- This subnet is OK to DELETE
    'auth-bank-lb-2a' : 'subnet-0d7c649028828be42',
    # 10.0.231.0/24 -- This subnet is OK to DELETE
    'auth-bank-lb-2c' : 'subnet-0faf5bf3ea4b0f3b8',
    # 10.0.44.0/24
    'auth-bank-phone-2a' : 'subnet-0078546f7cdb2b2fb',
    # 10.0.45.0/24
    'auth-bank-phone-2c' : 'subnet-0dc689153628d2abf',
    # 10.0.232.0/24
    'auth-phone-lb-2a' : 'subnet-0c4d5cf7db209c982',
    # 10.0.233.0/24
    'auth-phone-lb-2c' : 'subnet-0f71513b4a00e586a',
    # 10.0.40.0/24
    'chart-2a' : 'subnet-0b231faab99b58916',
    # 10.0.41.0/24
    'chart-2c' : 'subnet-0d6c1720c7c798ce6',
    # 10.0.240.0/23 USE THIS SUBNET FOR NEW INSTANCES
    'gdac-priv-2a' : 'subnet-0e4de6aeaec146f9d',
    # 10.0.242.0/23 USE THIS SUBNET FOR NEW INSTANCES
    'gdac-priv-2c' : 'subnet-0ac2fd214572da533',
    # 10.0.58.0/24 USE THIS SUBNET FOR EXT LB's and IGW's
    'gdac-pub-2a' : 'subnet-0874459c94225928c',
    # 10.0.59.0/24 USE THIS SUBNET FOR EXT LB's and IGW's
    'gdac-pub-2c' : 'subnet-0249213b05ddb6804',
    # 172.17.128.0/24, 2406:da12:503:ef80::/64
    'bip_private_2a' : 'subnet-0969f45ad9b40c4d2',
    # 172.17.129.0/24, 2406:da12:503:ef81::/64
    'bip_private_2c' : 'subnet-01b37f908063f0bcd',
    # 172.17.0.0/24, 2406:da12:503:ef00::/64
    'bip_public_2a' : 'subnet-09c36da1a637e3803',
    # 172.17.1.0/24, 2406:da12:503:ef01::/64
    'bip_public_2c' : 'subnet-0422b54b9b09a43b4',
    # 172.17.2.0/24, 2406:da12:503:ef02::/64
    'peer-pub-2a' : 'subnet-05a0132a446e3f672',
    # 172.17.3.0/24, 2406:da12:503:ef03::/64
    'peer-pub-2c' : 'subnet-0fff3a4163536101b',
    # 172.17.4.0/23, 2406:da12:503:ef04::/64
    'peer-pri-2a' : 'subnet-00db9886fe3ee9944',
    # 172.17.6.0/23, 2406:da12:503:ef06::/64
    'peer-pri-2c' : 'subnet-0dceda0b4eea4178c'
}


## IAM Profiles ###

iam_profile_dict = {
    'ec2-for-eb' : 'arn:aws:iam::762015387773:instance-profile/aws-elasticbeanstalk-ec2-role',
    'collectd' : 'arn:aws:iam::762015387773:instance-profile/phoenix-cw-collectd'
}


### Network InterfaceId

eni_dict = {
    'hashivault' : 'eni-012345abcde',
    'gl-batch-0' : 'eni-0109a57a635e52678'
}


### Security Groups ###

sec_group_dict = {
    'admin' : 'sg-045f867664e934ef5',
    'access' : 'sg-0ff2c47aa6c9ae9b1',
    'access-lb' : 'sg-014abd9c990a60307',
    # SG for external LB in EB beta-access
    'access-beta-lb' : 'sg-05007cc718f2f7e87',
    # SG for internal LB in EB beta-access
    'access-beta-vpn' : 'sg-07e2de238e56f99cd',
    'allow-jenkins-ssh' : 'sg-03099ff78f2237d6c',
    'auroradb' : 'sg-0d65ee7687c8f713e',
    'auth-bank' : 'sg-0ff4be5abf6b216b1',
    'auth-kakaopay' : 'sg-0887556a61ef5aacd',
    'auth-phone' : 'sg-0dc28fc1da2cb8748',
    'beta-access' : 'sg-03fa09c316c3079d7',
    'beta-access-lb' : 'sg-05007cc718f2f7e87',
    'bitgo' : 'sg-07ea0671591ef9e95',
    'blockinpress-db' : 'sg-0ba99aa3fe0fe33bf',
    'blockinpress-lb' : 'sg-01e15a460ced65824',
    'blockinpress-web' : 'sg-05dcdba0395e47233',
    'cmt' : 'sg-05b34fe57973d9389',
    'common-lcd' : 'sg-0f70d8710e0f5fb7b',
    'cosmos' : 'sg-06b14814dd5802bed',
    'cosmos-lcd' : 'sg-047bbf56362a67c78',
    'cruiser' : 'sg-0f67ec07a2658ed28',
    'deconomy' : 'sg-021dc7ebad9d8aaaf',
    'event-batch' : 'sg-021f565ca8828463e',
    'front' : 'sg-008e94c04a74b39ae',
    'front-lb' : 'sg-0676b9158bba9f1f2',
    'fx' : 'sg-0a36066465bd3533c',
    'geth' : 'sg-065e36c7d24367b4b',
    'gl-batch' : 'sg-0e6f1bdb751a8ea31',
    'gmart-api' : 'sg-0b1ec0d1736474636',
    'gmart-api-lb' : 'sg-05134dcdc9e3b1c83',
    'gmart-dealer' : 'sg-0b229286a64599395',
    'grow' : 'sg-043fc8f3492806d4a',
    'grow-blockeye' : 'sg-0ff66ed9c5cfff9da',
    'grow-dealer' : 'sg-0c974093ba0d21039',
    'grow-reward' : 'sg-0ce37e1ba35acc632',
    'hashivault' : 'sg-0b1e76b69ad651038',
    'hashtower-web' : 'sg-02605519d489f2ebc',
    'hashtower-web-lb' : 'sg-00f5240a03004ad9a',
    'internal-api' : 'sg-0701706f9b3cd39d7',
    'jenkins' : 'sg-024bc3efdb1595070',
    'match' : 'sg-0baa89bfe9674afa8',
    'notify' : 'sg-08b7b37eb5cd85e50',
    'openapi' : 'sg-0e08a30052b295812',
    'openapi-lb' : 'sg-0d56c4c576dd71eee',
    'orderbook' : 'sg-04de31c7688c455e1',
    'orderbook-lb' : 'sg-0f8cb9837ae09fbda',
    'orderbook-pub' : 'sg-0a612cbf2c04f79e2',
    'orderbook-pub-lb' : 'sg-0f3c28e23ac44b500',
    'partner' : 'sg-0ce3f515907845efb',
    'partner-lb' : 'sg-06d45c10eac18dfa6',
    'pay-orderbot' : 'sg-0712b0ce5c1874fee',
    'pd' : 'sg-038c5c3341a7ae97e',
    'peertec-web' : 'sg-06909efaf1d100890',
    'porsche' : 'sg-07434c721bac1ffd7',
    'porsche-lb' : 'sg-0bf9d5aa619076b8f',
    'sauron' : 'sg-04ba9c1b1a4d7f8da',
    'stats-dashboard' : 'sg-025ef459fd12d088c',
    'tx-verifier' : 'sg-00352b2f02a00af0c',
    'vault-blockeye' : 'sg-054f5cbdd55a9c2bf',
    # SG for internal LB forwarding web traffic from VPN
    'vpn-lb' : 'sg-0b239b13f8f104a6b',
    'wallet-cmt' : 'sg-0bf005f2423575d3c',
    'wallet-cosmos' : 'sg-0a3b19ab2cb3311eb',
    'wallet-eth' : 'sg-08789e8660f08b809',
    'wallet-iris' : 'sg-0d8158f328ac7c4d9',
    'wallet-terra' : 'sg-0dfd6de568edb67d8',
    'wireguard' : 'sg-05a78db63f7b0f3e3',
    'wireguard-http' : 'sg-0e6e3b041134c5d18',
    'wireguard-https' : 'sg-0f661bdc684289127',
    'wireguard-ng' : 'sg-0bbb125923301d6a0',
    'wireguard-peer' : 'sg-04c736735d811b0be',
    'wireguard-peer-ssh' : 'sg-013a07163581f036c',
    'wireguard-ssh' : 'sg-0caf05543766643d3'
}


### SSH Keys ###

ssh_keys_dict = {
    'auth-bank' : 'phoenix-auth-bank',
    'auth-bank-ng': 'auth-bank-ng',
    'bip' : 'bip-20181127',
    'event_batch' : 'event_batch',
    'final-test' : 'final_test',
    'front' : 'phoenix-front',
    'fx' : 'fx',
    'grow' : 'grow',
    'hashtower' : 'hashtower-20190510',
    'klaytn' : 'klayprod',
    'log' : 'phoenix-log',
    'monitor' : 'prod-monitor',
    'paybot-prod' : 'paybot-prod',
    'pd' : 'pd-node',
    'peertec-generic' : 'peertec-generic',
    'sauron' : 'sauron',
    'sky' : 'sky',
    'wallet' : 'phoenix-wallet',
    'wireguard-prod-ng' : 'wireguard-prod-ng',
    'wireguard-bip-ng' : 'wireguard-bip-ng',
    'wireguard-gdac' : 'wireguard-gdac',
    'wireguar-peer' : 'wireguard-peer'

}


### EC2 InstanceId's mapped to Human-Readable Names

# can also contain hostnames (for on-prem servers)
instance_id_dict = {
    'admin' : 'i-0825192ca4004ccd4',
    'auth-bank' : 'i-0e09d22b0f2dd0623',
    'auth-kakaopay' : 'i-0283993354e5f90d0',
    'bip-deconomy' : 'i-0dcff0c683d18c123',
    'bip-mysql' : 'i-0e6dfeac1955fe2cc',
    'bip-web' : 'i-0cd48e8e4bf695dfa',
    'bitgo-api' : 'i-050393dc55990f509',
    'bitgo-webhook' : 'i-06c52642bc5e313e8',
    'certmanager' : 'i-0d85be5f21fb397b2',
    'cmt': 'i-01f3a4f4532572b4b',
    'cosmos-lcd' : 'i-06ac2bb2633df9ebe',
    'cruiser': 'i-0d91abc420670b5d7',
    'eth-classic': 'i-0655fc87bf20d6551',
    'fr-1' : 'i-0e347a9272823a3f9',
    'fr-2' : 'i-03dfae244d013ac87',
    'fr-3' : 'i-06761262934f6f473',
    'fr-4' : 'i-0d1d151fa33038c25',
    'fr-alpha' : 'i-0cf018ad8819dfaa2',
    'fr-beta' : 'i-077cf36dfb8e59a3a',
    'fr-maintenance' : 'i-00353b3ec4203bf49',
    'fx' : 'i-0c14a23982d9b3000',
    'genesis' : 'gemesis',
    'geth1': 'i-0c1b71630b5299470',
    'geth2' : 'i-0a484d2c887b3cbde',
    'gl-batch-0' : 'i-0a5a65a1b0160f1f8',
    'gl-batch-1' : 'i-0d8b597c15fa4bab0',
    'gl-batch-2' : 'i-0b698a67b76b84fb5',
    'grow-vault' : 'i-012bdff808b747fe2',
    'hashivault' : 'i-0aaf98e89ff74df1b',
    'hashtower-web' : 'i-005e9ead348d847f8',
    'hdac' : 'i-09b24140b43a88485',
    'irisnet-full' : 'i-04f99172406fbc792',
    'irisnet-lcd' : 'i-07b2431465892b2ce',
    'jenkins' : 'i-0970d37f641904762',
    'klaytn' : 'i-059451cc9d6605137',
    'ledger' : 'i-024dd3062a1003ccd',
    'match0' : 'i-0cf1ec20a9da23de1',
    'pay-orderbot' : 'i-0fcaaaad22e7c7df1',
    'pd-analysis' : 'i-0b73e0349e61cc9f9',
    'peertec-prod' : 'i-0fc36d077905c4aee',
    'PL-batch' : 'i-0e57ff2eccc31c8af',
    'sauron' : 'i-0b083f0ab5e512eba',
    'service-admin' : 'i-06e57efbde249d63f',
    'stat-dashboard' : 'i-0177360cd61ba66e1',
    'terralcd' : 'i-045d94d85439fbdb1',
    'terrafull' : 'i-054182d222370b65a',
    'tx-veri' : 'i-0e8459ab2f3fa0e0f',
    'wg-prod' : 'i-059d9d4e0ff851ab6',
    'wg-bip' : 'i-024988dc373e49f91',
    'wallet' : 'i-01b6b888ded09f07e',
    'wg-gdac-2a' : 'i-07834f595ac366f27',
    'wg-peer-2a' : 'i-0106eb11613a5c3bb'
}


### Elastic Beanstalk Application Names

eb_application_dict = {
    'eb_app_myapp' : 'pjmart'
}

eb_app_acc_svr = 'acc-svr'  # for envo prod-access
eb_app_delmoondo_chart = 'delmoondo-chart'
eb_app_gmart = 'gmart'
eb_app_notifier = 'notifier'
eb_app_openapi = 'open-api-svr'
eb_app_porsche = 'Porsche'
eb_app_whalex_auth = 'whalex_auth'
eb_app_whalex_chart = 'whalex_chart'
eb_app_whalex_odr = 'whalex_orderbook'


### Elastic Beanstalk Environment Names

eb_environment_dict = {
    'auth-bank' : 'auth-bank',
    'auth-phone' : 'auth-phone',
    'beta-access' : 'beta_access_PROD',
    'chart-affogato' : 'prod-delmoondo-chart-affogato-b',
    'chart-latte' : 'prod-delmoondo-chart-latte',
    'chart-pub' : 'chart-pub',
    'gmart-api' : 'gmart-api',
    'gmart-dealer' : 'gmart-dealer',
    'notifier' : 'notifier-prod',
    'odr-pub' : 'odr-pub',
    'odr-svr' : 'odr-svr',
    'openapi' : 'openAPI-gdac',
    'porsche-api' : 'porsche-api',
    'prod-access' : 'prod-access'
}


### Auto Scaling Groups

asg_dict = {
    'asg_pjmart' : 'awseb-e-abc1234-stack-AWSEBAutoScalingGroup-foo',
}

asg_auth_bank = 'awseb-e-x8nrag2pyt-stack-AWSEBAutoScalingGroup-7J8A21UZIJX2'
asg_auth_phone = 'awseb-e-wxjgehjid2-stack-AWSEBAutoScalingGroup-1XZYEJZV8QZWY'
asg_chart_affo_b = 'awseb-e-qbvbvss3ti-stack-AWSEBAutoScalingGroup-21ANDRTELKC8'
asg_chart_latte = 'awseb-e-7cvmyr9pvx-stack-AWSEBAutoScalingGroup-1V5DDT4AWUYMD'
asg_chart_pub = 'awseb-e-wycse2pgsz-stack-AWSEBAutoScalingGroup-1EOR1VSCZ1KMP'
asg_gmart_api = 'awseb-e-9npkciqvmk-stack-AWSEBAutoScalingGroup-1V3DJU2474SUE'
asg_gmart_dealer = 'awseb-e-wpeav3t7rx-stack-AWSEBAutoScalingGroup-BC96P2YYQXYW'
asg_notifier_prod = 'awseb-e-m7ivbyetu34-stack-AWSEBAutoScalingGroup-1A6STHPOUKA07'
asg_odr_pub = 'awseb-e-pcdmfrnuyh-stack-AWSEBAutoScalingGroup-14YPT3FIMX6RZ'
asg_odr_svr = 'awseb-e-kjb4jx7q6a-stack-AWSEBAutoScalingGroup-O8EM6CXHALA8'
asg_porsche_api = 'awseb-e-wpeav3t7rx-stack-AWSEBAutoScalingGroup-BC96P2YYQXYW'
asg_prod_access = 'awseb-e-wmmhbffwi4-stack-AWSEBAutoScalingGroup-3Y5ZZMGL5BEZ'
asg_openapi = 'awseb-e-wwzt2ipmgv-stack-AWSEBAutoScalingGroup-9W0ILCL1JAKG'


## Load Balancers

# Note that 'elb_front' and 'elb_maintenance' are actually then
# same Load Balancer except that they use different target groups


#TODO: 'target-grp' should technically be nested under 'listeners'
# but for now target groups are the same for ALL listeners

load_balancer_dict = {
    'access' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/awseb-AWSEB-6HFS06ESU6OL/46ae5bb6cbcc012b',
        'lb-dns' : 'awseb-AWSEB-6HFS06ESU6OL-1337940674.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/awseb-AWSEB-15XOVKPUC2JTQ/752914777502546f',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-6HFS06ESU6OL/46ae5bb6cbcc012b/6b7f9e710c434604',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-6HFS06ESU6OL/46ae5bb6cbcc012b/9dbcfa1116db1340'
        },
    },

    'access-beta' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/awseb-AWSEB-1A9V0DZRJ4DBM/59b0a75d967d67b6',
        'lb-dns' : 'awseb-AWSEB-1A9V0DZRJ4DBM-2138011404.ap-northeast-2.elb.amazonaws.com',
        # Note that target-grp for access-beta and access-beta-internal
        # are different; but both should contain the same instances
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/awseb-AWSEB-1NWWH4TZCAGX9/9980242b9ae88abe',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1A9V0DZRJ4DBM/59b0a75d967d67b6/dd11aeef7b0f6b30',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1A9V0DZRJ4DBM/59b0a75d967d67b6/350aec9cba04e8e9'
        },
    },

    'access-beta-internal' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/beta-access-vpn-lb/c36f9ae19fa2b510',
        'lb-dns' : 'internal-beta-access-vpn-lb-229488242.ap-northeast-2.elb.amazonaws.com',
        # Note that target-grp for access-beta and access-beta-internal
        # are different; but both should contain the same instances
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/beta-access-grp-for-vpn/97ebbb79a6289886',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/beta-access-vpn-lb/c36f9ae19fa2b510/f25ac83e8709d179',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/beta-access-vpn-lb/c36f9ae19fa2b510/e9bff98b9c41373c'
        },
    },

    'blockinpress' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/blockinpress-internet-facing-lb/58aafeff01cafed5',
        'lb-dns' : 'blockinpress-internet-facing-lb-1245180215.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/blockinpress-web/ca5c703aca1d46ca',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/blockinpress-internet-facing-lb/58aafeff01cafed5/505ecad046200503',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/blockinpress-internet-facing-lb/58aafeff01cafed5/849e1112383356e5'
        },
    },

    'front' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/gdac-front-lb/e53e973804494272',
        'lb-dns' : 'gdac-front-lb-1103163120.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/front-servers/47ba406c33c8b24f',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/gdac-front-lb/e53e973804494272/138ff6cfaea4199c',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/gdac-front-lb/e53e973804494272/378c4ef6d7ff9100'
        },
    },

    'fwd-whalex' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/prod-whalex-traffic-forwarding/3c4ab0f16a8fb6d2',
        'lb-dns' : 'prod-whalex-traffic-forwarding-1488505001.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : '',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/prod-whalex-traffic-forwarding/3c4ab0f16a8fb6d2/eddfad0bc279db1e',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/prod-whalex-traffic-forwarding/3c4ab0f16a8fb6d2/b9da050cc2643ce0'
        }
    },

    'gmart-api' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/awseb-AWSEB-14VBVAFJJKVC4/f44824341aa80a65',
        'lb-dns' : 'awseb-AWSEB-14VBVAFJJKVC4-321644127.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/awseb-AWSEB-1JWYVJ17YRKVV/cef74ad076a636a1',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-14VBVAFJJKVC4/f44824341aa80a65/0ad10bf05b36c01b',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-14VBVAFJJKVC4/f44824341aa80a65/adf1121351a441aa'
        }
    },

    'hashtower-web' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/hashtower-web/dfb833d6d09a9dec',
        'lb-dns' : 'hashtower-web-1631225530.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/hashtower-web-target-grp/30bfaa64b62a4fff',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/hashtower-web/dfb833d6d09a9dec/07d4164d0124bffc',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/hashtower-web/dfb833d6d09a9dec/fe8544f28d94790d'
        }
    },

    'maintenance' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/gdac-front-lb/e53e973804494272',
        'lb-dns' : 'gdac-front-lb-1103163120.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/front-maintenance/27ebb6476c97cfd0',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/gdac-front-lb/e53e973804494272/138ff6cfaea4199c',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/gdac-front-lb/e53e973804494272/378c4ef6d7ff9100'
        }
    },

    'openapi' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/awseb-AWSEB-1EE3WIU9XYWYS/62b6bc7b72bf35cf',
        'lb-dns' : 'awseb-AWSEB-1EE3WIU9XYWYS-1505839169.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/awseb-AWSEB-1LKMCS1X0SJD7/02b5022cb03ba6fe',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1EE3WIU9XYWYS/62b6bc7b72bf35cf/eb058dcfc9e8ebd4',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1EE3WIU9XYWYS/62b6bc7b72bf35cf/e04391dc62d4d704'
        }
    },

    'partner-api' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/awseb-AWSEB-1828IJ0B5QWT8/e4e59bbd87a9cc80',
        'lb-dns' : 'awseb-AWSEB-1828IJ0B5QWT8-889473049.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/awseb-AWSEB-1D3O92HO1ARX0/0c741cb5d5f7248d',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1828IJ0B5QWT8/e4e59bbd87a9cc80/509ff5cbe263ec28',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/awseb-AWSEB-1828IJ0B5QWT8/e4e59bbd87a9cc80/059ecb97e99dda5a'
        }
    },

    'vpn-lb' : {
        'lb-arn' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:loadbalancer/app/general-vpn-lb/73fe678e82c874de',
        'lb-dns' : 'internal-general-vpn-lb-790759764.ap-northeast-2.elb.amazonaws.com',
        'target-grp' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:targetgroup/openapi-grp-for-vpn/f8caae5dfaa16c9d',
        'listeners' : {
            'http' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/general-vpn-lb/73fe678e82c874de/a07c31269f5938a9',
            'https' : 'arn:aws:elasticloadbalancing:ap-northeast-2:762015387773:listener/app/general-vpn-lb/73fe678e82c874de/5805f4333b08af81'
        }
    }
}

## ssl certificates
cert_dict = {
    'actwo-crt-arn':    'arn:aws:acm:ap-northeast-2:762015387773:certificate/19ce221c-5132-4b3d-b7d5-3608336ab82a',
    'bip-crt-arn':      'arn:aws:acm:ap-northeast-2:762015387773:certificate/f8f9de27-38a9-4715-ba0c-238d9ab5c910',
    'deconomy-crt-arn': 'arn:aws:acm:ap-northeast-2:762015387773:certificate/958e237e-1bed-412a-bb6e-cf96ba6365e4',
    'gdac-crt-arn':     'arn:aws:acm:ap-northeast-2:762015387773:certificate/d7865a9e-2f1d-4149-b170-99cac7c9b4a0',
    'hashtower-crt-arn':'arn:aws:acm:ap-northeast-2:762015387773:certificate/6f7ead3c-7701-49b6-9835-bde45e5d3132',
    'whalex-crt-arn':   'arn:aws:acm:ap-northeast-2:762015387773:certificate/243a4c20-4054-4ac9-9004-6cf928246799'
}

### Amazon Resource Numbers for SNS Topics
#note: prod-front-x are using the old 'front-gdac' SNS topic

sns_topic_dict = {
    'admin' : 'arn:aws:sns:ap-northeast-2:762015387773:admin-tonghap-noti',
    'auth-bank' : 'arn:aws:sns:ap-northeast-2:762015387773:auth-bank',
    'auth-bank-cw' : 'arn:aws:sns:ap-northeast-2:762015387773:auth-bank_cloudwatch_logs',
    'auth-phone' : 'arn:aws:sns:ap-northeast-2:762015387773:auth-phone',
    'bip-deconomy' : 'arn:aws:sns:ap-northeast-2:762015387773:bip-deconomy',
    'fx' : 'arn:aws:sns:ap-northeast-2:762015387773:fx',
    'geth' : 'arn:aws:sns:ap-northeast-2:762015387773:eth-svr-phnx_noti',
    'genesis' : 'arn:aws:sns:ap-northeast-2:762015387773:genesis-onprem',
    'grow-vault' : 'arn:aws:sns:ap-northeast-2:762015387773:grow-vault',
    'hdac' : 'arn:aws:sns:ap-northeast-2:762015387773:hdac-noti',
    'hashivault' : 'arn:aws:sns:ap-northeast-2:762015387773:hashivault-prod',
    'terrafull' :'arn:aws:sns:ap-northeast-2:762015387773:terra-full',
    'terralcd' : 'arn:aws:sns:ap-northeast-2:762015387773:terra-lcd',
    'PL-batch' : 'arn:aws:sns:ap-northeast-2:762015387773:PL-batch',
    'service-admin' : 'arn:aws:sns:ap-northeast-2:762015387773:service-admin',
    'jenkins' : 'arn:aws:sns:ap-northeast-2:762015387773:jenkins',
    'klaytn' : 'arn:aws:sns:ap-northeast-2:762015387773:klaytn',
    'irisnet-full' : 'arn:aws:sns:ap-northeast-2:762015387773:irisnet-full',
    'irisnet-lcd' : 'arn:aws:sns:ap-northeast-2:762015387773:irisnet-lcd',
    'cosmos-lcd' : 'arn:aws:sns:ap-northeast-2:762015387773:cosmos-lcd',
    'pay-orderbot' : 'arn:aws:sns:ap-northeast-2:762015387773:pay-orderbot',
    'sauron' : 'arn:aws:sns:ap-northeast-2:762015387773:sauron',
    'sns_ledger' : 'arn:aws:sns:ap-northeast-2:762015387773:ledger-tonghap-phoenix',
    'stat-dashboard' : 'arn:aws:sns:ap-northeast-2:762015387773:stat-dashboard',
    'stat-dashboard-cw' : 'arn:aws:sns:ap-northeast-2:762015387773:stat-dashboard-cloudwatch',
    'tx-veri' : 'arn:aws:sns:ap-northeast-2:762015387773:tx-veri'
}

sns_admin_tonghap = 'arn:aws:sns:ap-northeast-2:762015387773:admin-tonghap-noti'
sns_auth_bank = 'arn:aws:sns:ap-northeast-2:762015387773:auth-bank'
sns_auth_bank_cw = 'arn:aws:sns:ap-northeast-2:762015387773:auth-bank_cloudwatch_logs'
sns_auth_kakao = 'arn:aws:sns:ap-northeast-2:762015387773:kakaopay'
sns_auth_kakao_cw = 'arn:aws:sns:ap-northeast-2:762015387773:auth-kakaopay_cloudwatch_logs'
sns_auth_phone = 'arn:aws:sns:ap-northeast-2:762015387773:auth-phone'
sns_auth_phone_cw = 'arn:aws:sns:ap-northeast-2:762015387773:auth-phone_cloudwatch_logs'
sns_beta_access_cw = 'arn:aws:sns:ap-northeast-2:762015387773:beta_access_PROD'
sns_bitgo_api = 'arn:aws:sns:ap-northeast-2:762015387773:bitgo-api'
sns_bitgo_webhook = 'arn:aws:sns:ap-northeast-2:762015387773:bitgo-webhook'
sns_blockinpress = 'arn:aws:sns:ap-northeast-2:762015387773:blockinpress-noti'
sns_chart_svr = 'arn:aws:sns:ap-northeast-2:762015387773:chart-server-EB'
sns_chart_svr_cw = 'arn:aws:sns:ap-northeast-2:762015387773:chart-svr_cloudwatch_logs'
sns_cmt = 'arn:aws:sns:ap-northeast-2:762015387773:cmt'
sns_cruiser = 'arn:aws:sns:ap-northeast-2:762015387773:cruizer_noti'
sns_etc_classic = 'arn:aws:sns:ap-northeast-2:762015387773:etc-prod-noti'
sns_gmart_api = 'arn:aws:sns:ap-northeast-2:762015387773:gmart-api'
sns_gmart_dealer = 'arn:aws:sns:ap-northeast-2:762015387773:gmart-dealer'
sns_kakaopay = 'arn:aws:sns:ap-northeast-2:762015387773:kakaopay'
sns_maint = 'arn:aws:sns:ap-northeast-2:762015387773:front_maintenance'
sns_match0 = 'arn:aws:sns:ap-northeast-2:762015387773:match-0-phoenix'
sns_notifier = 'arn:aws:sns:ap-northeast-2:762015387773:notifier-prod'
sns_odr_pub = 'arn:aws:sns:ap-northeast-2:762015387773:odr-pub'
sns_odr_pub_cw = 'arn:aws:sns:ap-northeast-2:762015387773:odr-pub_cloudwatch_logs'
sns_odr_svr = 'arn:aws:sns:ap-northeast-2:762015387773:odr-svr'
sns_odr_svr_cw = 'arn:aws:sns:ap-northeast-2:762015387773:odr-svr_cloudwatch_logs'
sns_openapi = 'arn:aws:sns:ap-northeast-2:762015387773:openAPI-gdac'
sns_openapi_cw = 'arn:aws:sns:ap-northeast-2:762015387773:openapi_cloudwatch_logs'
sns_porsche = 'arn:aws:sns:ap-northeast-2:762015387773:porsche'
sns_prod_access = 'arn:aws:sns:ap-northeast-2:762015387773:access-gdac_cloudwatch_logs'
sns_prod_front = 'arn:aws:sns:ap-northeast-2:762015387773:front-gdac'
sns_prod_db_phnx = 'arn:aws:sns:ap-northeast-2:762015387773:prod-db-phoenix'
sns_prod_db_phnx_ap_ne_2c = 'arn:aws:sns:ap-northeast-2:762015387773:prod-db-phoenix-ap-northeast-2c-noti'
sns_ssl_cert = 'arn:aws:sns:ap-northeast-2:762015387773:ssl_cert_manager_svr'
sns_wallet = 'arn:aws:sns:ap-northeast-2:762015387773:wallet-svr-phnx'
sns_wireguard_bip = 'arn:aws:sns:ap-northeast-2:762015387773:wireguard-bip'
sns_wireguard_prod = 'arn:aws:sns:ap-northeast-2:762015387773:wireguard-prod'


### CIDR IP List (SG안에 집어 넣었는)

# 밑에 있는 cidr 변수들은 prod 운영망 계정에서만 볼 수 있음
cidr_dict = {
    'any-ip6' : '::/0',
    'any-ip' : '0.0.0.0/0',
    'candy-crawler' : '13.125.103.201/32',
    'candy-crawler-orderbook' : '13.125.50.250/32',
    'candy-crawler-price' : '15.164.144.41/32',
    'candy-db-redis' : '13.209.227.148/32',
    'candy-deploy' : '13.209.222.12/32',
    'candy-halls' : '13.209.253.236/32',
    'candy-halls-cow' : '52.78.3.173/32',
    'candy-ricola' : '13.124.182.139/32',
    'cloudbric-1' : '52.193.180.251/32',
    'cloudbric-2' : '54.180.69.235/32',
    'cloudbric-3' : '54.191.101.15/32',
    'nat-gw-2a' : '13.124.216.13/32',
    'nat-gw-2c' : '13.125.143.33/32',
    'nat-gw-dmz' : '13.125.157.3/32',
    'office' : '14.63.69.75/32',
    'pecunian-tokyo' : '52.68.110.249/32',
    'vpc-gdac' : '10.0.0.0/16',
    'wg-office' : '14.63.69.81/32'
}


### EBS VolumeId

ebs_vol_dict = {
    'admin-root' : 'vol-04418b6fde363602a',
    # rollback version from 2019.05.15
    'auth-bank-root' : 'vol-059bea1ea64832713',
    'bitgo-api-root' : 'vol-04bc2d9cedcfef1b6',
    'bitgo-webhook-clone-root' : 'vol-05723958127721314',
    'bitgo-webhook-vol' : 'vol-025b0a1f43e5de11c',
    'blockinpress-mysql' : 'vol-0aa39191ad87ec7f1',
    'blockinpress-root' : 'vol-0ebaa5fab2fc916a8',
    'peertecweb-root' : 'vol-0aa135f8507984a8b',
    'certmanager-root' : 'vol-0049a12d1d0b5884f',
    'cmt-root' : 'vol-0ea90d7094cc190d6',
    'cosmos-lcd-root' : 'vol-0dca197c3a0ce98ec',
    'cruiser-root' : 'vol-0073671c9c797a225',
    'deconomy-root' : 'vol-06579f2049f76183d',
    'etc-root' : 'vol-0f17b0329ab6ce584',
    'front1-root' : 'vol-0ca94de57c7219400',
    'front2-root' : 'vol-0ee9dbafb14dc366c',
    'front-alpha-root' : 'vol-0cbf40ee43f132aae',
    'front-beta-root' : 'vol-0698ef2d86ffdb09f',
    'fx' : 'vol-06e07ef9a8be66cc5',
    'geth1-root' : 'vol-08ebce2a43cbb25ad',
    'geth1-vol' : 'vol-0f539465c7b74c88a',
    'geth2-root' : 'vol-0260453bc95660bae',
    'geth2-vol' : 'vol-0a2e8301858257be1',
    'gl-batch0-root' : 'vol-0938d879a1ecb278b',
    'gl-batch1-root' : 'vol-061eec04f9db275a4',
    'gl-batch2-root' : 'vol-04f2fadeef6d2b49b',
    'grow-blockeye-root' : 'vol-0fb2c136b72407c21',
    'grow-dealer-root' : 'vol-0842e8115a5e8fbb0',
    'grow-reward-root' : 'vol-0d1fe1e57c179cdcb',
    'grow-vault-root' : 'vol-0634e480cbcc0e1dc',
    'hashivault-root' : 'vol-0dbec4e2afb87bc0e',
    'hashtower-root' : 'vol-0a82dacc760d34ef7',
    'hdac-root' : 'vol-0a24f82db34c6b1b2',
    'internal-api-root' : 'vol-03822a1e645c40044',
    'irisnet-full-root' : 'vol-0cb244a098db2ffa9',
    'irisnet-lcd-root' : 'vol-0201b8cad2afef120',
    'jenkins-root' : 'vol-007b63983203af787',
    'kakaopay-root' : 'vol-0edc11acbe47a1a8b',
    'ledger-root' : 'vol-04c70e76f14a47d5a',
    'ledger-sdb' : 'vol-06770df0f8da93bf0',
    'logger-root' : 'vol-05041721d7f3a4f1f',
    'maintenance-root' : 'vol-05e235e03483a6da4',
    'match-root' : 'vol-0a203d9ef54e31b47',
    'match-log' : 'vol-0902dc3dcc6a0addf',
    'pay-orderbot-root' : 'vol-0cf1c2035783082e8',
    'peertec-prod' : 'vol-08479b2fe06f6852f',
    'pl-batch0-root' : 'vol-0e1bb626dfc659cc3',
    'service-admin-root' : 'vol-097bba009bddaf584',
    'statdashb-root' : 'vol-0384725a440469d19',
    'terrafull-root' : 'vol-05e44fddd8bc5ffa6',
    'terralcd-root' : 'vol-0a7661d467e58f864',
    'wallet-root' : 'vol-0c7d67097423a5dce',
    'tx-verifier-root' : 'vol-0230ac66d295c1b4f',
    'event_batch' : 'vol-vol-096f4aad90a54e8f6',
    'sauron-root' : 'vol-03f9128d2242d332c',
    'gdac-beta-exchage-front-new' : 'vol-0c1c8ac2dd6cbc6b8',
    'wg-gdac-2a-root' : 'vol-01a7854cdaa1b95b8',
    'wg-peer-2a-root' : 'vol-0baa141ae147a0fb6'
}
