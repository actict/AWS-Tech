#!/usr/bin/env python3
# delete_elastic_beanstalk_envo.py
#
# Last Updated: 2018.12.04
# Updated by: scott.hwang@peertec.com
#
# This script will delete an Elastic Beanstalk environment name
# passed in as an argument on the command line. This script only
# works on instances in the PROD envo.


import argparse
import boto3
import sys


parser = argparse.ArgumentParser(
    description="Delete an Elastic Beanstalk environment matching "
                "an EB environment name passed as an argument.")
parser.add_argument('envoName', type = str, help = "name of EB "
                    "environment you want to delete")
args = parser.parse_args()

session = boto3.Session(profile_name = 'prod')
ebClient = session.client('elasticbeanstalk')

ck_envo_name = input("If you are sure you want to delete this EB environment"
                     "type its full name:\n")
if ck_envo_name != args.envoName:
    print("ERROR: environment name mismatch")
    sys.exit(1)
else:
    resp = ebClient.terminate_environment(
        EnvironmentName = args.envoName,
    )
    print(resp)
