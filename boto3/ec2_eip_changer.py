#!/usr/bin/env python3
# ec2_eip_changer.py
#
# Last Updated: 2018.08.12
# Updated by: scott.hwang@peertec.com
#
# Given an AWS EC2 'InstanceId' with Elastic IP, allocate a new EIP
# and associate the EIP with the EC2 instance


import argparse
import boto3
from botocore.exceptions import ClientError, BotoCoreError


def main():
    parser = argparse.ArgumentParser(
        description="Given an EC2 InstanceId, allocate a new EIP "
                    "and associate it with the instance.")
    parser.add_argument('insId', type=str, help="'InstanceId' as a "
                        "string between quotes.")
    args = parser.parse_args()

    ec2Client = boto3.client('ec2')
    #ec2Resource = boto3.resource('ec2')
    myNewEIP = ec2Client.allocate_address(Domain = 'vpc')

    print("### Associate new EIP with instance %s ###" % args.insId)

    try:
        assocResult = ec2Client.associate_address(
            AllocationId = myNewEIP['AllocationId'],
            InstanceId = args.insId,
            AllowReassociation = True)
        print("### Success: AssociationId: " + assocResult['AssociationId'])
    except (ValueError, ClientError, BotoCoreError) as e:
        print(e)


if __name__ == '__main__':
    main()
