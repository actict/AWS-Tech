#!/usr/bin/env python3
# create_all_cloudwatch_ec2_alarms_for_geth.py
#
# Last Updated: 2019.05.17
# Updated by: scott.hwang@peertec.com
#
# This script will create CPU, Memory, root disk, secondary disk,
# status and process alarms for EC2 servers running the geth daemon
# in AWS PROD envo. Such servers include geth1, geth2, and ETC.


import boto3
import time
from lib_cloudwatch_alarms import create_ec2_status_alarm
from lib_cloudwatch_alarms import create_collectd_cpu_alarm
from lib_cloudwatch_alarms import create_collectd_mem_alarm
from lib_cloudwatch_alarms import create_collectd_root_disk_alarm
from lib_cloudwatch_alarms import create_collectd_nonroot_disk_alarm
from lib_cloudwatch_alarms import create_collectd_process_alarm
from lib_cloudwatch_alarms import check_response_status
from env_prod import sns_topic_dict, instance_id_dict


def main():
    start = time.time()
    dictOfInst = {
        # 'key' is instance alias
        # 'key-value' is list containing the following fields:
        # (1) sns topic name (2) instance id (3) collectd name
        # of 2nd hard disk (4) list of collectd process names
        'geth1' : [sns_topic_dict['geth'], instance_id_dict['geth1'],
                   'opt-ethereum', ['geth', 'cloudwatch']],
        'geth2' : [sns_topic_dict['geth'], instance_id_dict['geth2'],
                   'opt-ethereum', ['geth', 'cloudwatch']],
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

        print("Creating disk alarm for secondary disk on %s" % mykey)
        # Note: the args for the function below are (1) cloudwatch client obj,
        # (2) inst name (3) sns topic, (4) instance id, (5) name of disk in
        # collectd (6) diskname you want to use in collectd-cw alarm
        resp5 = create_collectd_nonroot_disk_alarm(cwClient,
                                                   mykey,
                                                   dictOfInst[mykey][0],
                                                   dictOfInst[mykey][1],
                                                   dictOfInst[mykey][2],
                                                   mykey+dictOfInst[mykey][2]
                                                   )
        check_response_status(resp5)
    end = time.time()
    print("This script ran in %s seconds." %(end - start))


if __name__ == "__main__":
    main()
