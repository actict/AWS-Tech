#!/usr/bin/env python3
# env_validator_prod.py
#
# Last Updated: 2019.04.30
# Updated by: scott.hwang@peertec.com
#
# This program validates the environment variables contained in
# env_prod.py and returns a warning to stdout when AWS resources
# referenced by variable cannot be found.


import boto3
from env_prod import vpc_dict, subnet_dict, iam_profile_dict
from env_prod import sec_group_dict, ssh_keys_dict,instance_id_dict
from env_prod import sns_topic_dict, load_balancer_dict


def checkVPC(ec2cobj, mydict):
    """
    boto3 ec2 client object, dict -> stdout

    Given a boto3 ec2 client object 'ec2cobj' and a dict containing
    vpc names as keys and vpc IDs as keyvals, print a warning to
    stdout if the IDs cannot be found in AWS.
    """
    resp = ec2cobj.describe_vpcs()
    vpcL = list()

    for vpc in resp['Vpcs']:
        vpcL.append(vpc['VpcId'])
    for k in mydict:
        if mydict[k] in vpcL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### VPC ID for %s not found! ###" %k)
            print("%s does not exist!" %mydict[k])
            print("###################################")


def checkSubnet(ec2cobj, mydict):
    """
    boto3 ec2 client object, dict -> stdout

    Given a boto3 ec2 client object 'ec2cobj' and a dict containing
    subnet names as keys and subnet IDs as keyvals, print a warning to
    stdout if the IDs cannot be found in AWS.
    """
    resp = ec2cobj.describe_subnets()
    subnetL = list()

    for sn in resp['Subnets']:
        subnetL.append(sn['SubnetId'])

    for k in mydict:
        if mydict[k] in subnetL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### SubnetID for %s not found! ###" %k)
            print("%s does not exist!" %mydict[k])
            print("###################################")


def checkIAM(ec2cobj, mydict):
    """
    boto3 ec2 client object, dict -> stdout

    Given a boto3 ec2 client object 'ec2cobj' and a dict containing
    IAM profile names as keys and ARNs as keyvals, print a warning to
    stdout if the ARNs cannot be found in AWS.
    """
    resp = ec2cobj.describe_iam_instance_profile_associations()
    iam_arnL = list()

    for iam in resp['IamInstanceProfileAssociations']:
        iam_arnL.append(iam['IamInstanceProfile']['Arn'])

    for k in mydict:
        if mydict[k] in iam_arnL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### IAM ARN for %s not found! ###" %k)
            print("arn %s does not exist!" %mydict[k])
            print("###################################")


def checkSecGroup(ec2cobj, mydict):
    """
    boto3 ec2 client object, dict -> stdout

    Given a boto3 ec2 client object 'ec2cobj' and a dict containing EC2
    security group names as keys and IDs as keyvals, print a warning
    to stdout if the IDs cannot be found in AWS.
    """
    resp = ec2cobj.describe_security_groups()
    sec_groupL = list()

    for sg in resp['SecurityGroups']:
        sec_groupL.append(sg['GroupId'])

    for k in mydict:
        if mydict[k] in sec_groupL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### Security Group for %s not found! ###" %k)
            print("%s does not exist!" %mydict[k])


def checkSSH(ec2cobj, mydict):
    """
    boto3 ec2 client object, dict -> stdout

    Given a boto3 ec2 client object 'ec2cobj' and a dict containing ssh
    keynames as keys and AWS keyname IDs as keyvals, print a warning
    to stdout if the IDs cannot be found in AWS.
    """
    resp = ec2cobj.describe_key_pairs()
    keypairL = list()

    for skey in resp['KeyPairs']:
        keypairL.append(skey['KeyName'])

    for k in mydict:
        if mydict[k] in keypairL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### Key for %s not found! ###" %k)
            print("ssh keypair with name %s does not exist!" %mydict[k])
            print("#############################")


def checkInstanceID(ec2resobj, mydict):
    """
    boto3 ec2 resource object, dict -> stdout

    Given a boto3 ec2 resource object 'ec2resobj' and a dict containing
    instance names as keys and instance IDs as keyvals, print a warning
    to stdout if the IDs cannot be found in AWS.
    """
    instL = list()

    for inst in ec2resobj.instances.all():
        instL.append(inst.id)

    for k in mydict:
        if mydict[k] in instL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### InstanceID for %s not found! ###" %k)
            print("InstanceId %s does not exist!" %mydict[k])
            print("####################################")


def checkSNS(snsobj, mydict):
    """
    boto3 sns client object, dict -> stdout

    Given a boto3 sns client object 'snsobj' and a dict containing
    SNS topic names as keys and ARNs as keyvals, print a warning
    to stdout if the ARNs cannot be found in AWS.
    """
    resp = snsobj.list_topics()
    snsTopicsL = list()

    for elem in resp['Topics']:
        snsTopicsL.append(elem['TopicArn'])

    for k in mydict:
        if mydict[k] in snsTopicsL:
            print("%s for %s OK" %(mydict[k], k))
        else:
            print("### SNS topic for %s not found! ###" %k)
            print("ARN %s does not exist!" %mydict[k])
            print("###################################")


def checkLoadBalancer(elbv2obj, mydict):
    """
    boto3 elbv2 client object, dict -> stdout

    Given a boto3 elbv2 client object 'elbv2obj' and a dict containing
    LB names as keys and a nested dict containing 'lb-arn', 'lb-dns',
    etc. as keyvals, print a warning to stdout if the an 'lb-arn' cannot
    be found in AWS.
    """
    resp = elbv2obj.describe_load_balancers()
    lb_arnL = list()

    for elem in resp['LoadBalancers']:
        lb_arnL.append(elem['LoadBalancerArn'])

    for k in mydict:
        if mydict[k]['lb-arn'] in lb_arnL:
            print("%s for %s OK" %(mydict[k]['lb-arn'], k))
        else:
            print("### LB ARN for %s not found! ###" %k)
            print("ARN %s does not exist!" %mydict[k]['lb-arn'])
            print("###################################")


def main():
    session = boto3.Session(profile_name = 'prod')
    ec2Client = session.client('ec2')
    ec2Resource = session.resource('ec2')
    elb2Client = session.client('elbv2')
    snsClient = session.client('sns')

    print("### Checking VPC's in env_prod.py ###")
    checkVPC(ec2Client, vpc_dict)
    print("")
    print("### Checking Subnets in env_prod.py ###")
    checkSubnet(ec2Client, subnet_dict)
    print("")
    print("### Checking IAM roles in env_prod.py ###")
    checkIAM(ec2Client, iam_profile_dict)
    print("")
    print("### Checking Security Groups in env_prod.py ###")
    checkSecGroup(ec2Client, sec_group_dict)
    print("")
    print("### Checking SSH Keys in env_prod.py ###")
    checkSSH(ec2Client, ssh_keys_dict)
    print("")
    print("### Checking EC2 Instance ID's in env_prod.py ###")
    checkInstanceID(ec2Resource, instance_id_dict)
    print("")
    print("### Checking SNS topics in env_prod.py ###")
    checkSNS(snsClient, sns_topic_dict)
    print("")
    print("### Checking Load Balancers in env_prod.py ###")
    checkLoadBalancer(elb2Client, load_balancer_dict)


if __name__ == '__main__':
    main()
