#!/usr/bin/env python3
# create_all_cloudwatch_onprem_alarms_for_genesis.py
#
# Last Updated: 2019.05.20
# Updated by: scott.hwang@peertec.com
#
# This script will create CPU, Memory, root disk, and process alarms
# for the on-premises 'genesis' server running wireguard, dnsmasq, and
# other services in the Actwo offices in Seoul.


import boto3
import time
from lib_cloudwatch_alarms import create_collectd_cpu_alarm
from lib_cloudwatch_alarms import create_collectd_mem_alarm
from lib_cloudwatch_alarms import create_collectd_root_disk_alarm
from lib_cloudwatch_alarms import create_collectd_process_alarm
from lib_cloudwatch_alarms import check_response_status
from env_prod import sns_topic_dict


def main():
    start = time.time()
    dictOfInst = {
        # 'key' is instance alias 'key-value' is list containing the
        # following fields: (1) sns topic name (2) instance id or
        # hostname (3) collectd name of 2nd hard disk (4) list of
        # collectd process names
        'genesis' : [sns_topic_dict['genesis'], 'genesis',
                   '', ['wg-peer', 'wg-devnet', 'wg-gdac', 'wg-gate',
                        'dnsmasq', 'cloudwatch']],
    }

    session = boto3.Session(profile_name = 'prod')
    cwClient = session.client('cloudwatch')

    for mykey in dictOfInst:
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

    end = time.time()
    print("This script ran in %s seconds." %(end - start))


if __name__ == "__main__":
    main()
