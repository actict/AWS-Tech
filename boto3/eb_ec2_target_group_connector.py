#!/usr/bin/env python3
# eb_ec2_target_group_connector.py
#
# Last Updated: 2019.04.29
# Updated by: scott.hwang@peertec.com
#
# This boto3 script is intended to be executed whenever an Elastic
# Beanstalk app environment is updated. It adds an EC2 instance
# newly-created by EB to an instance target group attached to an
# internal Load Balancer. This script takes two arguments, the
# Elastic Beanstalk application environment name and the ARN of the LB
# target group. The third arg, '--profile' is optional: one of 'prod'
# or 'dev', with 'prod' as default (AWS CLI profile).


import argparse
import boto3
import sys


def addToTargetGroup(elbObj, tg, iid):
    """
    boto3 session object, string, string -> dict

    Given 'elbObj', a boto3 elbv2 client session object, 'tg' Target
    Group ARN as string, and 'iid' EC2 instance ID as string, add the
    EC2 instance to the given Target Group
    """
    resp = elbObj.register_targets(
        TargetGroupArn = tg,
        Targets = [
            {
                'Id': iid
            },
        ]
    )
    return resp


def getEC2FromEB(ebObj, appenvo_name):
    """
    boto3 session object, string -> list

    Given 'ebObj', a boto3 Elastic Beanstalk client session object and
    'appenvo_name', a string denoting the name of an EB app
    environment, return a list of EC2 instance ID's running in the EB
    app environment.
    """
    resp = ebObj.describe_environment_resources(
        EnvironmentName = appenvo_name)
    eb_ec2L = list()
    for i in resp['EnvironmentResources']['Instances']:
        eb_ec2L.append(i['Id'])
    return eb_ec2L


def check_response_status(mydict):
    """
    dict, string -> string to stdout

    Given a dict containing the HTTP Status Code response of a boto3
    request, print to stdout depending on the HTTP Status Code value
    """
    if mydict['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("creation SUCCESS")
    else:
        print("creation ERROR")


def main():
    # argparse boilerplate
    parser = argparse.ArgumentParser(
        description="Given an EB app environment name and the ARN "
        "of a LB target group, add EC2 instances from the EB app "
        "environment to the target group.")
    parser.add_argument('appenvo', type = str, help = "EB app envo name")
    parser.add_argument('lbtgarn', type = str, help = "ARN of Load Balancer "
                        "target group with target type 'instance'")
    parser.add_argument('--profile', type = str, nargs = '?',
                        default = 'prod', const = 'prod',
                        help = "optional argument, one of 'dev' or 'prod'.")
    args = parser.parse_args()


    # Input validation for args.lbtgarn
    if 'elasticloadbalancing' not in args.lbtgarn:
        print("Invalid Amazon Resource Number for LB!")
        sys.exit(1)

    # Create boto3 client sessions for Elastic Beanstalk and ELBv2
    session = boto3.Session(profile_name = args.profile)
    ebClient = session.client('elasticbeanstalk')
    elb2Client = session.client('elbv2')

    print("Getting EC2 Instance Id's from EB app environment %s..."
          % args.appenvo)
    ec2_in_eb_envoL = getEC2FromEB(ebClient, args.appenvo)
    if ec2_in_eb_envoL == None:
        print("Error! No EC2 instances in EB app environment %s!"
              % args.appenvo)
    for inst in ec2_in_eb_envoL:
        status = addToTargetGroup(elb2Client, args.lbtgarn, inst)
        check_response_status(status)


if __name__ == '__main__':
    main()
