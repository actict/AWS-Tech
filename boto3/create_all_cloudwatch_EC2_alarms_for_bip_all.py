#!/usr/bin/env python3
# create_all_cloudwatch_EC2_alarms_for_bip_all.py
#
# Last Updated: 2019.01.16
# Updated by: scott.hwang@peertec.com
#
# This script will create CPU, Memory, root disk, status and process
# alarms for all Blockinpress EC2 servers: bip-web, bip-mysql,
# bip-deconomy


import boto3
from lib_cloudwatch_alarms import *
from env_prod import *


def main():
    dictOfInst = {
        'bip-web' : [sns_blockinpress, iid_bip_web, '',
                       ['apache2']
        ],
        'bip-deconomy': [sns_blockinpress, iid_bip_deconomy, '',
                         ['apache2']
        ],
        'bip-mysql': [sns_blockinpress, iid_bip_mysql, 'var-lib-mysql',
                      ['mysql']
        ]
    }

    session = boto3.Session(profile_name = 'prod')
    cwClient = session.client('cloudwatch')

    for mykey in dictOfInst:
        print("Creating status alarm for server %s" % mykey)
        resp0 = create_ec2_status_alarm(cwClient, mykey,
                                        dictOfInst[mykey][0],
                                        dictOfInst[mykey][1])
        check_response_status(resp0)

        print("Creating CPU alarm for server %s" % mykey)
        resp1 = create_collectd_cpu_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp1)

        print("Creating memory alarm for server %s" % mykey)
        resp2 = create_collectd_mem_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp2)

        print("Creating root disk alarm for server %s" % mykey)
        resp3 = create_collectd_root_disk_alarm(cwClient, mykey,
                                                dictOfInst[mykey][0],
                                                dictOfInst[mykey][1])
        check_response_status(resp3)


        print("Creating process alarms for server %s" % mykey)
        for proc in dictOfInst[mykey][3]:
            print("Create alarm for process %s" % proc)
            resp4 = create_collectd_process_alarm(cwClient,
                                                  mykey,
                                                  dictOfInst[mykey][0],
                                                  dictOfInst[mykey][1],
                                                  proc)
            check_response_status(resp4)

    print("Creating disk alarm for secondary disk on bip-mysql")
    resp5 = create_collectd_nonroot_disk_alarm(cwClient,
                                               'bip-mysql',
                                               sns_blockinpress,
                                               dictOfInst['bip-mysql'][1],
                                               dictOfInst['bip-mysql'][2],
                                               'mysql-disk'
                                               )
    check_response_status(resp5)


if __name__ == "__main__":
    main()
