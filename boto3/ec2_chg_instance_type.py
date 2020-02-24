#!/usr/bin/env python3
# ec2_chg_instance_type.py
#
# Last Updated: 2018.09.02
# Updated by: scott.hwang@peertec.com
#
# This script takes three parameters:
# (1) AWS EC2 'InstanceId'
# (2) A valid EC2 'InstanceType' (i.e. 't2.micro', 'm5.large' ...)
# (3) aws environment profile alias
#
# It then stops the instance, changes the 'InstanceType', verifies
# that the 'InstanceType' has changed, and then starts the modified
# instance


import argparse
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import sys
import time


def check_state_stopped(instId, cliobj):
    """
    str, boto3 ec2Client object -> boolean

    Given str denoting 'InstanceId', return True if Instance
    state is 'stopped'
    """
    resp = cliobj.describe_instances(InstanceIds = [instId])
    state = resp['Reservations'][0]['Instances'][0]['State']['Name']
    return state == 'stopped'


def stop_instance(instId, cliobj):
    """
    str, boto3 ec2Client object -> dict

    Given a string denoting EC2 'InstanceId', stop the instance
    Returns a dict
    """
    resp = cliobj.stop_instances(InstanceIds = [instId])
    return resp


def modify_instance(instId, instType, cliobj):
    """
    str, str, boto3 ec2Client object -> dict

    Given strings denoting EC2 'InstanceId' and 'InstanceType', change
    the type of the EC2 instance to 'InstanceType'. Returns a dict
    """
    resp = cliobj.modify_instance_attribute(
        InstanceId = instId,
        InstanceType = {'Value': instType}
        )
    return resp


def start_instance(instId, cliobj):
    """
    str, boto3 ec2Client object -> dict

    Given a string denoting EC2 'InstanceId', start the instance
    Returns a dict
    """
    resp = cliobj.start_instances(InstanceIds = [instId])
    return resp


def instance_type_is_same(instId, instType, cliobj):
    """
    str, str, boto3 ec2Client object -> boolean

    Given strings denoting EC2 'InstanceId' and 'InstanceType', check
    that the instance has 'InstanceType' == instType. Returns boolean
    'True' or 'False'
    """
    resp = cliobj.describe_instances(InstanceIds = [instId])
    return resp['Reservations'][0]['Instances'][0][
        'InstanceType'] == instType


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
        description="Given an EC2 InstanceId and desired InstanceType, "
                    "modify the Instance to a new InstanceType.")
    parser.add_argument('iid', type = str, help = "'InstanceId' as a "
                        "string between quotes.")
    parser.add_argument('itype', type = str, help = "the desired "
                        "instance type")
    parser.add_argument('awsEnvo', type = str, help = "the name of "
                        "your desired AWSCLI environment. NOTE: "
                        "~/.aws/{config,credentials} must exist!")
    args = parser.parse_args()

    session = boto3.Session(profile_name = args.awsEnvo)
    ec2Client = session.client('ec2')

    print("### Check if InstanceType %s is the same as "
          "the existing type" % args.itype)
    if instance_type_is_same(args.iid, args.itype, ec2Client):
        print("ERROR: Please specify another InstanceType! The one "
              "you specified is the same as the existing type!")
        sys.exit(1)

    try:
        print("### Stopping Instance %s" % args.iid)
        stopResult = stop_instance(args.iid, ec2Client)
        print(stopResult['StoppingInstances'])
    except (ValueError, ClientError, BotoCoreError) as e:
        print(e)
        sys.exit(1)

    print("### Waiting until Instance %s fully stopped..." % args.iid)
    while not check_state_stopped(args.iid, ec2Client):
        time.sleep(1.0)
    print("Instance state is 'stopped'")

    try:
        print("### Modifying Instance %s to InstanceType %s" %(args.iid,
                                                               args.itype))
        modifyResult = modify_instance(args.iid, args.itype, ec2Client)
        print(stopResult['StoppingInstances'])
    except (ValueError, ClientError, BotoCoreError) as e:
        print(e)
        sys.exit(1)

    print("### Check that the modified InstanceType %s matches the "
          "requested type ###" % args.itype)
    if instance_type_is_same(args.iid, args.itype, ec2Client):
        print("SUCCESS: the requested InstanceType was correctly modified")
    else:
        print("ERROR: the requested InstanceType change has not been made!")
        sys.exit(1)

    try:
        print("### Starting Instance %s" %(args.iid))
        startResult = start_instance(args.iid, ec2Client)
        print(startResult['StartingInstances'])
    except (ValueError, ClientError, BotoCoreError) as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
