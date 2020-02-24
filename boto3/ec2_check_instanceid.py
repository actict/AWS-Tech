#!/usr/bin/env python3
# ec2_check_instanceid.py
#
# Last Updated: 2018.09.04
# Updated by: scott.hwang@peertec.com
#
# This script reads a file which contains InstanceId's and other
# info on every line. It then uses describe_instances() method
# from EC2 client in boto3 to return info about the given instances


import argparse
import boto3
import doctest


def get_instanceid(lol):
    """
    ListOfList -> ListOfString

    'lol' is a ListOfLists containing strings representing
    'InstanceId' and EC2 'InstanceType', respectively. This
     function returns a ListOfStrings composed of InstanceId's

    >>> get_instanceid([['i-08550d989b5d69421', 'c5.4xlarge']])
    ['i-08550d989b5d69421']
    """
    inztIdL = [lizt[0] for lizt in lol]
    return inztIdL


def get_instancetype(lol):
    """
    ListOfList -> ListOfString

    'lol' is a ListOfLists containing strings representing
    'InstanceId' and EC2 'InstanceType', respectively. This
     function returns a ListOfStrings composed of EC2
    InstanceTypes

    >>> get_instancetype([['i-08550d989b5d69421', 'c5.4xlarge']])
    ['c5.4xlarge']
    """
    inztTypeL = [lizt[1] for lizt in lol]
    return inztTypeL


def main():
    """
    First, call the function 'check_instance_type()' as a sanity check
    to make sure that the requested InstanceType is not identical to
    the existing one.

    Second, if (1) passes, call 'stop_instance()' and wait until stopped
    Third, call 'modify_instance()'
    Fourth, call 'check_instance_type()'
    Fifth, finally call 'start_instance()'
    """
    parser = argparse.ArgumentParser(
        description="Given a filename and AWS environment profile,"
        " return info about the instance.")
    parser.add_argument('fname', type = str, help = "Name of file containing "
                        "EC2 InstanceId's, one per line")
    parser.add_argument('awsEnvo', type = str, help = "the name of "
                        "your desired AWSCLI environment. NOTE: "
                        "~/.aws/{config,credentials} must exist!")
    args = parser.parse_args()

    session = boto3.Session(profile_name = args.awsEnvo)
    ec2Client = session.client('ec2')

    textL = list()
    print("### Reading file...")
    with open(args.fname, 'r') as f:
        textL = [line.rstrip().split() for line in f]
    print("### Removing firstline comment and empty lines")
    if '#' in textL[0]:
        del(textL[0])
    textL = list(filter(None, textL))
    listOfiid = get_instanceid(textL)

    print("### Printing Info for each InstanceId...")
    for id in listOfiid:
        resp = ec2Client.describe_instances(InstanceIds = [id])
        name = "No tag called 'Name'"
        for dict in resp['Reservations'][0]['Instances'][0]['Tags']:
            if dict['Key'] == 'Name':
                name = dict['Value']
                break

        if resp['Reservations'][0]['Instances'][0]['IamInstanceProfile']:
            IAMp = resp['Reservations'][0]['Instances'][0][
                'IamInstanceProfile']['Arn']
        else:
            IAMp = 'No IAM Profile Assigned'

        print("ID: %s, Name: %s, IAM Profile: %s" %(id, name, IAMp))
        print("")


if __name__ == '__main__':
    doctest.testmod()
    main()
