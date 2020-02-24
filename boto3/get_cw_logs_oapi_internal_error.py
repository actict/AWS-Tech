#!/usr/bin/env python3
# get_cw_logs_oapi_internal_error.py
#
# Last Updated: 2018.10.05
# Updated by: scott.hwang@peertec.com
#
# This script submits a query to AWS Cloudwatch Logs and returns
# logs from a given 'start' & 'end' window stated in UNIX Epoch Time
# x 1000 (UNIX epoch ms).
#
# This script takes the following arguments:
# (1) AWS environment name (specified in '~/.aws/credentials')
# (2) Cloudwatch Log Group name
# (3) filter pattern
# (4) start time in 'YYYY-MM-DD HH:mm:ss' (UTC)
# (5) end time in 'YYYY-MM-DD HH:mm:ss' (UTC)
# (6) filename in which to store search results
# (7) file to store the execution log for this script
#
# NOTE: this script has been customized to match the string
# '__internal_error__' for 'loglevel:[info]' events from
# 'openapi-gdac_logs' Cloudwatch Log group.


import argparse
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from datetime import datetime
import doctest
import logging
from logging.handlers import RotatingFileHandler


def human_to_epoch_ms(timestr):
    """
    str -> int

    Given a string in 'YYYY-MM-DD HH:mm:ss' format (UTC), return an
    int representing UNIX epoch time in milliseconds (i.e., epoch time
    * 1000)

    >>> human_to_epoch_ms('2018-09-21 03:15:00 GMT+0000')
    1537499700000

    >>> human_to_epoch_ms('1970-01-01 00:00:00 GMT+0000')
    0
    """
    dobj = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S GMT%z')
    epoch = dobj.timestamp()
    epochms = int(epoch * 1000)

    return epochms


def main():
    parser = argparse.ArgumentParser(
        description="Return Cloudwatch Logs matching a filter pattern "
                    "between time 'start' and 'end'.")
    parser.add_argument('awsEnvo', type = str, help = "name of your desired "
                        "aws envo from '~/.aws/credentials'")
    parser.add_argument('logGrp', type = str, help = "name of your Cloudwatch "
                        "Logs log group")
    parser.add_argument('filter', type = str, help = "pattern to use for "
                        "filtering logs")
    parser.add_argument('start', type = str, help = "start time in "
                        "'YYYY-MM-DD HH:mm:ss' UTC")
    parser.add_argument('end', type = str, help = "end time in "
                        "'YYYY-MM-DD HH:mm:ss' UTC")
    parser.add_argument('filename', type = str, help = "output filename "
                        "where results will be saved. Please use abs path.")
    parser.add_argument('logfile', type = str, help ="app log file. "
                        "Please use absolute path to file.")
    args = parser.parse_args()

    # Boilerplate for logging with log rotation and rollover
    # Max log file size is 1MB (1mio bytes), 4 rotating logs
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(args.logfile, maxBytes=1024000,
                                  backupCount=4)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s '
                                  '- %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # add UTC TZ to 'args.start' & 'args.end'
    args.start = args.start + ' GMT+0000'
    logger.debug("Start time in YYYY-MM-DD: %s" % args.start)
    args.end = args.end + ' GMT+0000'
    logger.debug("End time in YYYY-MM-DD: %s" % args.end)

    session = boto3.Session(profile_name = args.awsEnvo)
    logsClient = session.client('logs')
    paginator = logsClient.get_paginator('filter_log_events')

    resp_iterator = paginator.paginate(
        logGroupName = args.logGrp,
        startTime = human_to_epoch_ms(args.start),
        endTime = human_to_epoch_ms(args.end),
        filterPattern = args.filter,
        interleaved = True,
        PaginationConfig = {
            'MaxItems': 1000,
            'PageSize': 1000
        }
    )

    results = list(resp_iterator)
    logger.debug("All Log Events: %s" % results)

    # Unpack nested list of dicts...
    payload = results[0]['events']
    intErrorL =  list()

    for i in range(len(payload)):
        # the string below is only found in [info] loglevel
        # this will be changed to [error] loglevel in the future
        if "__internal_error__" in payload[i]['message']:
            intErrorL.append(payload[i]['message'])

    if len(intErrorL) > 0:
        with open(args.filename, 'w') as f:
            print()
            f.write('\n')
            for j in range(len(intErrorL)):
                print(intErrorL[j])
                f.write(intErrorL[j])
                print()
                f.write('\n')
    else:
        print()
        print("No results for search term!")
        # make results file 0 bytes
        with open(args.filename, 'w') as f:
            f.truncate()


if __name__ == '__main__':
    doctest.testmod()
    main()
