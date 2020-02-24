#!/usr/bin/env python3
# create_all_cloudwatch_EB_alarms_for_notifier-prod.py
#
# Last Updated: 2018.12.14
# Updated by: scott.hwang@peertec.com
#
# This boto3 script creates Cloudwatch Alarms for Elastic Beanstalk
# Application 'notifier', environment 'notifier-prod'. The alarms
# include:
#     (1) max CPU (from AutoScaling Group)
#     (2) EB Environment Health (load balancer health check pings)
#     (3) Max Root Disk Usage among all instances in EB Environment


import boto3
from env_prod import *
from lib_cloudwatch_alarms import *


session = boto3.Session(profile_name = 'prod')
cwClient = session.client('cloudwatch')
ebClient = session.client('elasticbeanstalk')


print("Enable 'RootFilesystemUtil' tracking every 60s in EB environment %s"
      % eb_env_notifier)

resp = ebClient.update_environment(
    ApplicationName = eb_app_notifier,
    EnvironmentName = eb_env_notifier,
    OptionSettings = [
        {
            'Namespace': 'aws:elasticbeanstalk:healthreporting:system',
            'OptionName': 'ConfigDocument',
            'Value': '{"Version":1,"CloudWatchMetrics":{"Instance":{"RootFilesystemUtil":60}}}'
        }
    ]
)
check_response_status(resp)


print("Create max disk usage alarm for EB envo %s" % eb_env_notifier)
resp1 = create_elastic_beanstalk_max_disk_usage_alarm(cwClient,
                                                      eb_env_notifier,
                                                      sns_notifier)
print(resp1)


print("Create max CPU usage alarm for EB envo %s" % eb_env_notifier)
resp2 = create_elastic_beanstalk_max_cpu_alarm(cwClient,
                                               eb_env_notifier,
                                               sns_notifier,
                                               asg_notifier_prod)
print(resp2)


print("Create EB envo health status alarm for %s" % eb_env_notifier)
resp3 = create_elastic_beanstalk_health_alarm(cwClient,
                                              eb_env_notifier,
                                              sns_notifier)

print(resp3)
