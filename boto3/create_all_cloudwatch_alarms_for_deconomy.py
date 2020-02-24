#!/usr/bin/env python3
# create_all_cloudwatch_alarms_for_deconomy.py
#
# Last Updated: 2019.09.16
# Updated by: scott.hwang@peertec.com, scott.hwang@actwo.com
#
# This script will create CPU, Memory, root disk, and process alarms
# for all EC2 'deconomy' server running in AWS PROD Seoul region.

import boto3
import time
from lib_cloudwatch_alarms import create_collectd_cpu_alarm
from lib_cloudwatch_alarms import create_collectd_mem_alarm
from lib_cloudwatch_alarms import create_collectd_root_disk_alarm
from lib_cloudwatch_alarms import create_collectd_process_alarm
from lib_cloudwatch_alarms import check_response_status
from env_prod import sns_topic_dict, instance_id_dict


def main():
    start = time.time()
    dictOfInst = {
        # 'key' is instance alias 'key-value' is list containing the
        # following fields: (1) sns topic name (2) instance id or
        # hostname (3) collectd name of 2nd hard disk (4) list of
        # collectd process names
        'bip-deconomy' : [sns_topic_dict['bip-deconomy'],
                    instance_id_dict['bip-deconomy'], '',
                    ['cloudwatch', 'apache2']]
         }
    session = boto3.Session(profile_name = 'prod_cw_full')
    cwClient = session.client('cloudwatch')

    for mykey in dictOfInst:
        print("Creating CPU alarm for server %s" % mykey)
        resp1 = create_collectd_cpu_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp1)
        time.sleep(0.5)

        print("Creating memory alarm for server %s" % mykey)
        resp2 = create_collectd_mem_alarm(cwClient, mykey,
                                          dictOfInst[mykey][0],
                                          dictOfInst[mykey][1])
        check_response_status(resp2)
        time.sleep(0.5)

        print("Creating root disk alarm for server %s" % mykey)
        resp3 = create_collectd_root_disk_alarm(cwClient, mykey,
                                                dictOfInst[mykey][0],
                                                dictOfInst[mykey][1])
        check_response_status(resp3)
        time.sleep(0.5)

        print("Creating process alarms for server %s" % mykey)
        for proc in dictOfInst[mykey][3]:
            print("Create alarm for process %s" % proc)
            resp4 = create_collectd_process_alarm(cwClient,
                                                  mykey,
                                                  dictOfInst[mykey][0],
                                                  dictOfInst[mykey][1],
                                                  proc)
        check_response_status(resp4)
        time.sleep(0.5)

    end = time.time()
    print("This script ran in %s seconds." %(end - start))


if __name__ == "__main__":
    main()
