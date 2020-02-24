#!/usr/bin/env python3
# daily_ec2_basic_units.py
#
# Last Updated: 2019.05.22
# Updated by: scott.hwang@peertec.com
#
# This boto3 script gets information on all EC2 instances in the
# 'running' state in both PROD, DEV, and Pecunian accounts. It then
# calculates basic units for each instance type and presents the basic
# unit total across PROD, DEV, and Pecunian environments.


import boto3
import datetime
from daily_cost_report_prod import send_to_slack


def extract_ec2_units(ec2resobj):
    """
    ec2Resource Object -> dictOfInts

    Given a "session.resource('ec2')" object, return a dictOfInts
    containing the count of 't2.nano', 't3.nano', 'm4.large', 'm5.large',
    and 'c5.large' basic units for instances in the state 'running'.
    """
    resp = ec2resobj.instances.filter(
        Filters = [
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    retD = dict()
    # declare ec2 basic unit counters
    t2_nano_units, t3_nano_units, m4_large_units = 0, 0, 0
    m5_large_units, c5_large_units = 0, 0
    # dicts mapping ec2 instance type to number of basic units
    t2_nano_map = {'t2.nano': 1, 't2.micro': 2, 't2.small': 4,
                   't2.medium': 8, 't2.large': 16, 't2.xlarge': 32}
    t3_nano_map = {'t3.nano': 1, 't3.micro': 2, 't3.small': 4,
                   't3.medium': 8, 't3.large': 16, 't3.xlarge': 32}
    m4_large_map = {'m4.large': 1, 'm4.xlarge': 2, 'm4.2xlarge': 4}
    m5_large_map = {'m5.large': 1, 'm5.xlarge': 2, 'm5.2xlarge': 4}
    c5_large_map = {'c5.large': 1, 'c5.xlarge': 2, 'c5.2xlarge': 4}

    for inst in resp:
        instType = inst.instance_type
        if 't2' in instType:
            t2_nano_units += t2_nano_map[instType]
        elif 't3' in instType:
            t3_nano_units += t3_nano_map[instType]
        elif 'm4' in instType:
            m4_large_units += m4_large_map[instType]
        elif 'm5' in instType:
            m5_large_units += m5_large_map[instType]
        elif 'c5' in instType:
            c5_large_units += c5_large_map[instType]

    retD = {
        't2.nano': t2_nano_units,
        't3.nano': t3_nano_units,
        'm4.large': m4_large_units,
        'm5.large': m5_large_units,
        'c5.large': c5_large_units
    }

    return retD


def sum_ec2_units(*dictz):
    """
    dictOfInts, dictOfInts -> dictOfInts

    Given an arbitrary number of dicts in *dictv  with keys
    corresponding to EC2 basic instance types 't2.nano', 't3.nano',
    'm5.large' etc, and keyvals corresponding to integer counts for
    each basic instance type, combine the keyvalues for each instance
    type key.
    """
    valid_keys = ['t2.nano', 't3.nano', 'm4.large', 'm5.large',
                  'c5.large']
    total_cntD = dict()

    for k in valid_keys:
        mycnt = 0
        for mydict in dictz:
            mycnt += mydict.get(k, 0)
        total_cntD[k] = mycnt

    return total_cntD


def prez_ec2_units(dictOfInts, timeNow, outfile):
    """
    dictOfInts, str, str -> str (to stdout and file)

    Given 'dictOfInts' containing keys corresponding to instances types
    such as 't3.nano', 'm5.large', etc. and keyvals corresponding to
    counts of these instance types, return this info on stdout as well
    as writing this info to a file specified by 'outfile'. 'timeNow'
    is a 'datetime' converted to str format.
    """
    with open(outfile, 'w') as f:
        print("*EC2 INSTANCE BASIC UNITS COUNT* @ %s" % timeNow)
        f.write("*EC2 INSTANCE BASIC UNITS COUNT* @ %s\n" % timeNow)
        print("======================================================")
        f.write("======================================================\n")
        print("\t`t2.nano units count`:\t\t%d" % dictOfInts['t2.nano'])
        f.write("\t`t2.nano units count`:\t\t%d\n" % dictOfInts['t2.nano'])
        print("\t`t3.nano units count`:\t\t%d" % dictOfInts['t3.nano'])
        f.write("\t`t3.nano units count`:\t\t%d\n" % dictOfInts['t3.nano'])
        print("\t`m5.large units count`:\t\t%d" % dictOfInts['m5.large'])
        f.write("\t`m5.large units count`:\t\t%d\n" % dictOfInts['m5.large'])
        print("\t`c5.large units count`:\t\t%d" % dictOfInts['c5.large'])
        f.write("\t`c5.large units count`:\t\t%d\n" % dictOfInts['c5.large'])
        print("\t`m4.large units count`:\t\t%d" % dictOfInts['m4.large'])
        f.write("\t`m4.large units count`:\t\t%d\n" % dictOfInts['m4.large'])


def main():
    # datetime-related vars
    UTC = datetime.datetime.utcnow()
    KST = UTC + datetime.timedelta(days = 9/24) # KST is UTC + 9
    #EST = KST - datetime.timedelta(days = 1)
    TimeK = KST.strftime('%Y-%m-%d %H:%M')
    # file I/O-related vars
    file_path = '/home/ec2-user/bin/'
    outfile = file_path + 'ec2_basic_units_prod+dev_' + TimeK + '.txt'
    # boto3 session vars
    sessionP = boto3.Session(profile_name = 'prod_ce_full_ec2_ro')
    sessionD = boto3.Session(profile_name = 'dev_ce_full_ec2_ro')
    sessionPc = boto3.Session(profile_name = 'pecun_ce_full_ec2_ro')
    ec2ResourceP = sessionP.resource('ec2')
    ec2ResourcePc = sessionPc.resource('ec2')
    ec2ResourceD = sessionD.resource('ec2')
    # Slack-related vars
    slack_webhook = 'https://hooks.slack.com/services/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'

    ec2_units_prod = extract_ec2_units(ec2ResourceP)
    ec2_units_dev = extract_ec2_units(ec2ResourceD)
    ec2_units_pec = extract_ec2_units(ec2ResourcePc)
    ec2_units_total = sum_ec2_units(ec2_units_prod, ec2_units_dev,
                                    ec2_units_pec)

    prez_ec2_units(ec2_units_total, TimeK, outfile)

    print("Send EC2 Basic Unit Counts to to Slack")
    http_status = send_to_slack(outfile, slack_webhook,
                                'AWS_EC2_BASIC_UNITS_COUNT DEV+PROD')
    if http_status != 200:
        print("Sending EC2 Basic Unit Counts data payload to %s FAILED!"
              % slack_webhook)
    else:
        print("Sending AWS Cost Explorer data payload to %s SUCCESS!"
              % slack_webhook)


if __name__ == "__main__":
    main()
