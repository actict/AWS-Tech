#!/usr/bin/env python3
# create_all_cloudwatch_alarms_for_auth_phone.py
#
# Last Updated: 2019.03.20
# Updated by: scott.hwang@peertec.com
#
# This script will create CPU, Memory, root disk, status and process
# alarms for auth-phone Elastic Beanstalk instance


import boto3
from lib_cloudwatch_alarms import *
from env_prod import *


def main():
    dictOfInst = {
        'auth-phone' : [sns_auth_phone, iid_auth_phone, '',
                       ['authphonejs', 'nginx', 'cloudwatch']
        ],
    }

    session = boto3.Session(profile_name = 'prod')
    cwClient = session.client('cloudwatch')

    for mykey in dictOfInst:
        print("Creating status alarm for server %s" % mykey)
        resp0 = create_ec2_status_alarm(cwClient, mykey,
                                        dictOfInst[mykey][0],
                                        dictOfInst[mykey][1])
        check_response_status(resp0)
        print(resp0)

        print("Creating CPU alarm for server %s" % mykey)
        resp1 = create_collectd_cpu_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp1)
        print(resp1)

        print("Creating memory alarm for server %s" % mykey)
        resp2 = create_collectd_mem_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp2)
        print(resp2)

        print("Creating root disk alarm for server %s" % mykey)
        resp3 = create_collectd_root_disk_alarm(cwClient, mykey,
                                                dictOfInst[mykey][0],
                                                dictOfInst[mykey][1])
        check_response_status(resp3)
        print(resp3)


        print("Creating process alarms for server %s" % mykey)
        for proc in dictOfInst[mykey][3]:
            print("Create alarm for process %s" % proc)
            resp4 = create_collectd_process_alarm(cwClient,
                                                  mykey,
                                                  dictOfInst[mykey][0],
                                                  dictOfInst[mykey][1],
                                                  proc)
            check_response_status(resp4)
            print(resp4)


if __name__ == "__main__":
    main()
