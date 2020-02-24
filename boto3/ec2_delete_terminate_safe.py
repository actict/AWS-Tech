#!/usr/bin/env python3
# ec2_delete_terminate_safe.py
#
# Last Updated: 2019.06.11
# Updated by: scott.hwang@peertec.com
#
# This script takes an arbitrary number of space-separated instance
# ID's from the command line and will terminate each of the
# instances. Before rebooting, the user will be presented with the
# instance's tag 'Name:' and will have to type 'Yes' to confirm the
# reboot operation.


import argparse
import boto3


def getNameTag(eco, iid):
    """
    ec2ClientObject, str -> str

    Given an ec2 client object and ec2 instance ID as string, return
    the value for tag 'Name' from the JSON output of method
    describe_instances(). Returns a string
    """
    resp = eco.describe_instances(InstanceIds = [iid])
    list_of_tags = resp['Reservations'][0]['Instances'][0]['Tags']

    for d in list_of_tags:
        if d['Key'] == 'Name':
            inst_name = d['Value']
    return inst_name


def terminateInstance(eco, iid):
    """
    ec2ClientObject, str -> dict

    Given an ec2 client object and ec2 instance ID as string,
    terminate the instance using the method terminate_instances().
    Returns a dict containing http status code of the operation.
    """
    resp = eco.terminate_instances(InstanceIds = [iid])
    return resp


def main():
    # argparse boilerplate
    parser = argparse.ArgumentParser(
        description="Given an arbitrary number of space-separated EC2 "
        "instance ID's, return human-readable info for each ID and "
        "prompt the user to confirm each terminate operation.")
    parser.add_argument('iid', type = str, help = "instance ID w/o quotes",
                        nargs = '+')
    parser.add_argument('--profile', type = str, nargs = '?',
                        default = 'prod_ec2_full', const = 'prod_ec2_full',
                        help = "optional argument, AWS profile_name")
    args = parser.parse_args()

    session = boto3.Session(profile_name = args.profile)
    ec2Client = session.client('ec2')

    inst_cnt = 1
    for id in args.iid:
        inst_name = getNameTag(ec2Client, id)
        confirm = ''
        while confirm not in ('Yes', 'no'):
            confirm = input("Do you really want to terminate InstanceID "
                            "%s with Name %s?\n"
                            "Please type 'Yes' or 'no':\n"
                            %(id, inst_name))
        if confirm == 'Yes':
            print("## %d. Terminating InstanceID %s with Name %s ##"
                  %(inst_cnt, id, inst_name))
            delete_status = terminateInstance(ec2Client, id)
            http_stat = delete_status['ResponseMetadata']['HTTPStatusCode']
            if http_stat == 200:
                print("## Terminate request ACCEPTED 200 OK##")
            else:
                print("## Terminate request HTTP ERROR: %d" % http_stat)
        inst_cnt += 1


if __name__ == '__main__':
    main()
