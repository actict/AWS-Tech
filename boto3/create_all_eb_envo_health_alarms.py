#!/usr/bin/env python3
# create_all_eb_envo_health_alarms.py
#
# Last Updated: 2018.12.07
# Updated by: scott.hwang@peertec.com
#
# This script will create Elastic Beanstalk Health alarms for
# multiple EB environments. These alarms are based on Elastic
# Beanstalk load balancer health checks to instances.


import boto3
from lib_cloudwatch_alarms import *
from env_prod import *


def main():

    dictOfenv = {
        'auth-bank' : [eb_env_auth_bank, sns_auth_bank_cw],
        'auth-phone' : [eb_env_auth_phone, sns_auth_phone_cw],
        'beta-access' : [eb_env_beta_access, sns_beta_access_cw],
        'blue-pumpkin-order-svr' : [eb_env_blue_pumpkin_osvr,
                          sns_chart_svr_cw],
        'chart-affogato-b' : [eb_env_chart_affo_b, sns_chart_svr_cw],
        'chart-latte' : [eb_env_chart_latte, sns_chart_svr_cw],
        'gmart-api' : [eb_env_gmart_api, sns_gmart_api],
        'gmart-dealer' : [eb_env_gmart_dealer, sns_gmart_dealer],
        'notifier-prod': [eb_env_notifier_prod, sns_notifier],
        'odr-pub' : [eb_env_odr_pub_old, sns_odr_pub_cw],
        'odr-svr': [eb_env_odr_svr_old, sns_odr_svr_cw],
        'openapi' : [eb_env_openapi_gdac, sns_openapi_cw],
        'porsche-api' : [eb_env_porsche, sns_porsche],
        'prod-access' : [eb_env_prod_access, sns_prod_access]
        }

    session = boto3.Session(profile_name = 'prod')
    cwClient = session.client('cloudwatch')

    for mykey in dictOfInst:
        print("Creating status alarm for server %s" % mykey)
        resp0 = create_elastic_beanstalk_health_alarm(cwClient,
                                        dictOfenv[mykey][0],
                                        dictOfenv[mykey][1])
        check_response_status(resp0)

if __name__ == "__main__":
    main()
