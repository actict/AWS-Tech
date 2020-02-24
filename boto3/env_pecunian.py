#!/usr/bin/env python3
# env_pecunian.py
#
# Last Updated: 2019.05.22
# Updated by: scott.hwang@peertec.com
#
# File containing environment variables to be used in boto3 scripts
# provisioning resources in the AWS 'Pecunian' account.


vpc_dict = {
    'pecunian' : 'vpc-0df47a30495af8c76',
    # do not use the default vpc
    'pec-default' : 'vpc-0f86469eb63aac43c'
}


subnet_dict = {
    # 192.168.0.0/24
    'public-2a' : 'subnet-0deb4ee540fec7047',
    # 192.168.1.0/24
    'public-2c' : 'subnet-0d0432dbc4d25ebb5'
}


## IAM Profiles ###

iam_profile_dict = {
    'ec2-for-eb' : 'arn:aws:iam::964383167692:role/aws-elasticbeanstalk-ec2-role',
    'collectd' : 'arn:aws:iam::964383167692:role/pecunian-cw-collectd'
}


### Network InterfaceId

eni_dict = {}


### Security Groups ###

sec_group_dict = {
    'admin-repo' : 'sg-027d7d3dbdde8272d',
    'crawler' : 'sg-031b9c1e0c97aa612',
    'deploy' : 'sg-075b5902bd05e5428',
    'halls' : 'sg-0ecaffa5866a79cd1',
    'halls-cow' : 'sg-0970ef09b1dbf7c59',
    'ricola' : 'sg-052fef4981ade8a93',
    'wireguard-ssh' : 'sg-0ffc1ffe3616be5ce',
    'wireguard-udp' : 'sg-0d02d8e75a5ccdd75',
}


### SSH Keys ###

ssh_keys_dict = {
    'candy-seoul' : 'doncandy-seoul',
    'wireguard' : 'wg-pecunian'
}


### EC2 InstanceId's mapped to Human-Readable Names

# can also contain hostnames (for on-prem servers)
instance_id_dict = {
    'crawler' : 'i-07bf390ef4fb9eec7',
    'crawler-orderbook' : 'i-05a24545956adef8d',
    'crawler-price' : 'i-005030e10b8e8402f',
    'db-redis' : 'i-012692fb8196a8497',
    'deploy' : 'i-0014c93fa1ac73084',
    'halls' : 'i-0d3c28f71e58475c4',
    'halls-cow' : 'i-0dee2a708ce5388e4',
    'ricola' : 'i-009be07f4e0828a51',
    'wireguard' : 'i-0745a6950bdfdd05c'
}


### Elastic Beanstalk Application Names

eb_application_dict = {
    'candy-crawler' : 'sandbox-candy-crawler'
}


### Elastic Beanstalk Environment Names

eb_environment_dict = {
    'sandbox-crawler' : 'sandbox-candy-crawler',
}


### Auto Scaling Groups

asg_dict = {}


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
}

## ssl certificates
cert_dict = {}

### Amazon Resource Numbers for SNS Topics
#note: prod-front-x are using the old 'front-gdac' SNS topic

sns_topic_dict = {
    'crawler' : 'arn:aws:sns:ap-northeast-2:964383167692:crawler',
    'crawler-odrbk' : 'arn:aws:sns:ap-northeast-2:964383167692:crawler-odrbk',
    'crawler-price' : 'arn:aws:sns:ap-northeast-2:964383167692:crawler-price',
    'db-redis' : 'arn:aws:sns:ap-northeast-2:964383167692:db-redis',
    'candy-deploy' : 'arn:aws:sns:ap-northeast-2:964383167692:candy-deploy',
    'halls' : 'arn:aws:sns:ap-northeast-2:964383167692:halls',
    'halls-cow' : 'arn:aws:sns:ap-northeast-2:964383167692:halls-cow',
    'ricola' : 'arn:aws:sns:ap-northeast-2:964383167692:ricola'
}

sns_subs_dict = {
    'sl_notify_candy' : 'https://hooks.slack.com/services/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',
    'eml_emergency' : 'g8k2s3x6k3k9f9m6@whalex.slack.com'
}

### CIDR IP List (SG안에 집어 넣었는)

cidr_dict = {
    'any-ip6' : '::/0',
    'any-ip' : '0.0.0.0/0',
    'office' : '14.63.69.75/32',
    'wg-office' : '14.63.69.81/32'
}


### EBS VolumeId

ebs_vol_dict = {
    'crawler-root' : 'vol-0bd7ee55eb105f913',
    'crawler-order-root' : 'vol-010101c1a5ead6aaa',
    'crawler-price-root' : 'vol-07a9d17b38f23d3a3',
    'db-redis-root' : 'vol-01e63b15bbdb92844',
    'deploy-root' : 'vol-021596301ac3f4852',
    'halls-root' : 'vol-0a19cba5e889f2c7e',
    'halls-cow-root' : 'vol-0a19cba5e889f2c7e',
    'ricola-root' : 'vol-0ea996bf4427e9cf5',
    'wireguard-root' : 'vol-071d343648e2a8fd3'
}
