#!/usr/bin/env python3
# daily_cost_report_dev.py
#
# Last Updated: 2019.02.05
# Updated by: scott.hwang@peertec.com
#
# This boto3 script uses the AWS Cost Explorer API to query the
# billing data from the previous day for DEV envo. Extracted data
# includes the following:
# - A. Daily Bill by Service Type
#   + EC2 Instances
#   + EC2 Other
#   + EC2 Load Balancer
#   + Cloudwatch
#   + RDB Service
#   + Elasticache Redis
#   + SNS
# - B. Detailed line-item breakdown by Service Type (TODO)
#
# This script is almost identical to 'daily_cost_report_prod.py'
# except that it does not query Reserved Instance data;
# RI contracts are made in PROD envo account, and cover both PROD
# and DEV environments


import argparse
import boto3
import datetime
from decimal import Decimal
import json
import requests


def extract_ce(svc_dict, utype_dict):
    """
    dict, dict -> dict

    Given 'svc_dict', a nested dict of lists containing Cost Explorer
    (CE) data grouped by Service and 'utype_dict', a nested dict of
    lists containing CE data grouped by both Operation and Usage_Type,
    return a dict containing all non-RI CE billing data for 'EC2',
    'EC2-Other', 'Load Balancer', 'Cloudwatch', 'RDB', 'Elasticache',
    'S3', etc. and line items for each service.
    """
    res = dict()
    svcsList = [
        'EC2 - Other',
        'Amazon Elastic Compute Cloud - Compute',
        'Amazon Elastic Load Balancing',
        'Amazon Relational Database Service',
        'Amazon ElastiCache',
        'Amazon Route 53',
        'Amazon Simple Notification Service',
        'Amazon Simple Storage Service',
        'AmazonCloudWatch'
    ]
    # utypeList elements are created by joining the keyvals from
    # GroupBy 'OPERATION' and 'USAGE_TYPE' with the string ': '
    svc_to_utype = {
        'EC2 - Other':
        ['CreateSnapshot: APN2-EBS:SnapshotUsage',
         'CreateVolume: APN2-EBS:VolumeUsage',
         'CreateVolume-Gp2: APN2-EBS:VolumeUsage.gp2',
         'CreateVolume-P-IOPS: APN2-EBS:VolumeP-IOPS.piops',
         'CreateVolume-P-IOPS: APN2-EBS:VolumeUsage.piops',
         'EBS:IO-Read: APN2-EBS:VolumeIOUsage',
         'EBS:IO-Write: APN2-EBS:VolumeIOUsage',
         'NatGateway: APN2-NatGateway-Bytes',
         'NatGateway: APN2-NatGateway-Hours',
         'AssociateAddressVPC: APN2-ElasticIP:IdleAddress'
        ],

        'Amazon Elastic Compute Cloud - Compute':
        ['RunInstances: APN2-BoxUsage:c5.large',
         'RunInstances: APN2-BoxUsage:m5.large',
         'RunInstances: APN2-BoxUsage:m5.xlarge',
         'RunInstances:0002: APN2-BoxUsage:m4.large',
         'RunInstances: APN2-BoxUsage:t2.medium',
         'RunInstances: APN2-BoxUsage:t2.micro',
         'RunInstances: APN2-BoxUsage:t2.nano',
         'RunInstances: APN2-BoxUsage:t2.small',
         'RunInstances: APN2-BoxUsage:t3.medium',
         'RunInstances: APN2-BoxUsage:t3.micro',
         'RunInstances: APN2-BoxUsage:t3.nano'
         'RunInstances: APN2-BoxUsage:t3.small',
         'RunInstances: APN2-DataTransfer-Out-Bytes'
        ],

        'Amazon Route 53':
        ['NS: DNS-Queries',
         'MX: DNS-Queries',
         'A: DNS-Queries',
         'A: Intra-AWS-DNS-Queries',
         'AAAA: DNS-Queries',
         'ANY: DNS-Queries',
         'CAA: DNS-Queries',
         'CNAME: DNS-Queries',
         'TXT: DNS-Queries'
        ],

        'Amazon Elastic Load Balancing':
        ['LoadBalancing: APN2-DataProcessing-Bytes',
         'LoadBalancing: APN2-DataTransfer-In-Bytes',
         'LoadBalancing: APN2-DataTransfer-Out-Bytes',
         'LoadBalancing: APN2-LoadBalancerUsage',
         'LoadBalancing-PublicIP-Out: APN2-DataTransfer-Regional-Bytes',
         'LoadBalancing:Application: APN2-LCUUsage',
         'LoadBalancing:Application: APN2-LoadBalancerUsage'
        ],

        'Amazon Simple Storage Service':
        ['StandardIAStorage: APN2-TimedStorage-SIA-ByteHrs',
         'StandardStorage: APN2-TimedStorage-ByteHrs',
         'CompleteMultipartUpload: APN2-Requests-Tier1',
         'CopyObject: APN2-Requests-Tier1'
        ],

        'AmazonCloudWatch':
        ['Unknown: APN2-CW:AlarmMonitorUsage',
         'Unknown: APN2-CW:HighResAlarmMonitorUsage',
         'Unknown: CW:AlarmMonitorUsage',
         'PutLogEvents: APN2-DataProcessing-Bytes',
         'PutMetricData: APN2-CW:Requests',
         'MetricStorage: APN2-CW:MetricMonitorUsage',
         'MetricStorage:AWS/Beanstalk: APN2-CW:MetricMonitorUsage',
         'MetricStorage:AWS/CloudWatchLogs: APN2-CW:MetricMonitorUsage',
         'MetricStorage:AWS/EC2: APN2-CW:MetricMonitorUsage',
         'DashboardHour: DashboardsUsageHour-Basic',
         'DashboardHour: DashboardsUsageHour',
        ],

        'Amazon ElastiCache':
        ['CreateCacheCluster:0002: APN2-NodeUsage:cache.m4.xlarge'],

        'Amazon Relational Database Service':
        ['CreateDBInstance: APN2-Aurora:StorageIOUsage',
         'CreateDBInstance: APN2-Aurora:StorageUsage',
         'CreateDBInstance:0016: APN2-InstanceUsage:db.r4.xlarge'
        ],
    }


    lod0 = svc_dict['ResultsByTime'][0]['Groups']
    lod1 = utype_dict['ResultsByTime'][0]['Groups']

    #print("lod0 is %s" %lod0)
    for i in range(len(lod0)):
        service_name = lod0[i]['Keys'][0]
        if service_name in svcsList:
            res[service_name] = dict()
            res[service_name]['Cost'] = lod0[i]['Metrics'][
                'UnblendedCost']['Amount']
    #print("results dict is %s" %res)

    for j in range(len(lod1)):
        for k in svc_to_utype:
            #print("key from svc_to_utype is %s" %k)
            joinKeys = ': '.join(lod1[j]['Keys'])
            #print("joined Key is %s" %joinKeys)
            if joinKeys in svc_to_utype[k]:
                res[k][joinKeys] = lod1[j]['Metrics']['UnblendedCost']['Amount']

    return res


def prez_extract_ce(res_dict, rpt_date, outfile):
    """
    dictOfDict, str, str -> text to stdout, file

    This function will pretty print the grouped Cost Explorer results
    from extract_ce() to stdout and to a file. It 'presents' results
    in an easy-to-read format

    Note that extract_ce generates 'res_dict' from a combination of
    *cost by service* (coarse) and *cost by utilization type* (detailed).
    The dict structure from *cost by service* is different from that
    of the latter. To get cost data from the former, you must specify
    the key '<service name>', followed by key 'Cost', whereas getting
    cost data from *cost by utilization type* requires the key
    '<service name>' followed by the key '<custom utype string>'. In
    the latter, there is no key 'Cost'.

    Also note that all possible keys defined in 'extract_ce()' may not
    be represented in 'res_dict' on a given day. For example, if you
    are not using any 't2.nano' instances, the key
    'RunInstances: APN2-BoxUsage:t2.nano' will not exist.
    """
    ## EC2 COMPUTE
    ## from *cost by service* ##
    ec2_compute = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'][
            'Cost'])
    ##-----------------------------------------------------##
    ## from *cost by utilization type* ##
    ec2_compute_c5_large = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:c5.large', 0))
    ec2_compute_m5_large = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:m5.large', 0))
    ec2_compute_m5_xlarge = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:m5.xlarge', 0))
    ec2_compute_t2_medium = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t2.medium', 0))
    ec2_compute_t2_micro = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t2.micro', 0))
    ec2_compute_t2_nano = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t2.nano', 0))
    ec2_compute_t2_small = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t2.small', 0))
    ec2_compute_t3_medium = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t3.medium', 0))
    ec2_compute_t3_micro = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t3.micro', 0))
    ec2_compute_t3_nano = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t3.nano', 0))
    ec2_compute_t3_small = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t3.small', 0))
    ec2_compute_egress_data = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-DataTransfer-Out-Bytes',0))
    ec2_compute_m4_large_mswin = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances:0002: APN2-BoxUsage:m4.large', 0))
    ##-----------------------------------------------------##

    ## EC2 OTHER
    ## from *cost by service ##
    ec2_other = Decimal(res_dict['EC2 - Other']['Cost'])
    ##-----------------------------------------------------##
    ## from *cost by utilization type* ##
    ec2_other_idle_eip = Decimal(res_dict['EC2 - Other'].get(
        'AssociateAddressVPC: APN2-ElasticIP:IdleAddress', 0))
    ec2_other_ebs_snapshot_usage = Decimal(res_dict['EC2 - Other'].get(
        'CreateSnapshot: APN2-EBS:SnapshotUsage', 0))
    ec2_other_ebs_vol_usage = Decimal(res_dict['EC2 - Other'].get(
        'CreateVolume: APN2-EBS:VolumeUsage', 0))
    ec2_other_ebs_vol_usage_gp2 = Decimal(res_dict['EC2 - Other'].get(
        'CreateVolume-Gp2: APN2-EBS:VolumeUsage.gp2', 0))
    ec2_other_ebs_vol_piops_reserve = Decimal(res_dict['EC2 - Other'].get(
        'CreateVolume-P-IOPS: APN2-EBS:VolumeP-IOPS.piops', 0))
    ec2_other_ebs_vol_piops_size = Decimal(res_dict['EC2 - Other'].get(
        'CreateVolume-P-IOPS: APN2-EBS:VolumeUsage.piops', 0))
    ec2_other_ebs_io_read = Decimal(res_dict['EC2 - Other'].get(
        'EBS:IO-Read: APN2-EBS:VolumeIOUsage', 0))
    ec2_other_ebs_io_write = Decimal(res_dict['EC2 - Other'].get(
        'EBS:IO-Write: APN2-EBS:VolumeIOUsage', 0))
    ec2_other_nat_gw_bytes = Decimal(res_dict['EC2 - Other'].get(
        'NatGateway: APN2-NatGateway-Bytes', 0))
    ec2_other_nat_gw_hours = Decimal(res_dict['EC2 - Other'].get(
        'NatGateway: APN2-NatGateway-Hours', 0))
    ##-----------------------------------------------------##

    ## RELATIONAL DATABASE SERVICE
    ## from *cost by service* ##
    rdb_service = Decimal(res_dict['Amazon Relational Database Service'][
        'Cost'])
    ##-----------------------------------------------------##
    ## from *cost by utilization type* ##
    rdb_aurora_storage_io = Decimal(res_dict[
        'Amazon Relational Database Service'].get(
            'CreateDBInstance: APN2-Aurora:StorageIOUsage', 0))
    rdb_aurora_storage_usage = Decimal(res_dict[
        'Amazon Relational Database Service'].get(
            'CreateDBInstance: APN2-Aurora:StorageUsage', 0))
    rdb_instance_usage_db_r4_xlarge = Decimal(res_dict[
        'Amazon Relational Database Service'].get(
            'CreateDBInstance:0016: APN2-InstanceUsage:db.r4.xlarge', 0))

    ## CLOUDWATCH
    ## from *cost by service* ##
    cloudwatch = Decimal(res_dict['AmazonCloudWatch']['Cost'])
    ##-----------------------------------------------------##
    ## from *cost by utilization type* ##
    cw_apn2_alarm_mon_usage = Decimal(res_dict['AmazonCloudWatch'].get(
        'Unknown: APN2-CW:AlarmMonitorUsage', 0))
    cw_apn2_highres_alarm_mon_usage = Decimal(res_dict['AmazonCloudWatch'].get(
        'Unknown: APN2-CW:HighResAlarmMonitorUsage', 0))
    cw_alarm_mon_usage = Decimal(res_dict['AmazonCloudWatch'].get(
        'Unknown: CW:AlarmMonitorUsage', 0))
    cw_put_log_events = Decimal(res_dict['AmazonCloudWatch'].get(
        'PutLogEvents: APN2-DataProcessing-Bytes', 0))
    cw_put_metric_data_req = Decimal(res_dict['AmazonCloudWatch'].get(
        'PutMetricData: APN2-CW:Requests', 0))
    cw_metric_storage_mon_usage = Decimal(res_dict['AmazonCloudWatch'].get(
        'MetricStorage: APN2-CW:MetricMonitorUsage', 0))
    cw_metric_storage_beanstalk_mon_usage = Decimal(
        res_dict['AmazonCloudWatch'].get(
            'MetricStorage:AWS/Beanstalk: APN2-CW:MetricMonitorUsage', 0))
    cw_metric_storage_cw_logs_mon_usage = Decimal(
        res_dict['AmazonCloudWatch'].get(
            'MetricStorage:AWS/CloudWatchLogs: APN2-CW:MetricMonitorUsage', 0))
    cw_metric_storage_ec2_apn2_metric_mon_usage = Decimal(
        res_dict['AmazonCloudWatch'].get(
            'MetricStorage:AWS/EC2: APN2-CW:MetricMonitorUsage', 0))
    cw_dashboard_usage_basic = Decimal(res_dict['AmazonCloudWatch'].get(
        'DashboardHour: DashboardsUsageHour-Basic', 0))
    cw_dashboard_usage = Decimal(res_dict['AmazonCloudWatch'].get(
        'DashboardHour: DashboardsUsageHour', 0))

    ## ELASTICACHE
    ## from *cost by service* ##
    ecredis = Decimal(res_dict['Amazon ElastiCache']['Cost'])
    ##-----------------------------------------------------##
    ## *from cost by utilization type* ##
    ecredis_cache_m4_xlarge = Decimal(res_dict['Amazon ElastiCache'].get(
        'CreateCacheCluster:0002: APN2-NodeUsage:cache.m4.xlarge', 0))
    ##-----------------------------------------------------##

    ## ELASTIC LOAD BALANCER
    ## from *cost by service* ##
    ec2_elb = Decimal(res_dict['Amazon Elastic Load Balancing']['Cost'])
    ##-----------------------------------------------------##
    ## from *cost by utilization type*
    elb_data_processing_bytes = Decimal(res_dict[
        'Amazon Elastic Load Balancing'].get(
            'LoadBalancing: APN2-DataProcessing-Bytes', 0))
    elb_egress_bytes = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
        'LoadBalancing: APN2-DataTransfer-Out-Bytes', 0))
    elb_egress_regional_bytes = Decimal(res_dict[
        'Amazon Elastic Load Balancing'].get(
            'LoadBalancing-PublicIP-Out: APN2-DataTransfer-Regional-Bytes', 0))
    elb_lcu_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
        'LoadBalancing:Application: APN2-LCUUsage', 0))
    elb_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
        'LoadBalancing: APN2-LoadBalancerUsage', 0))
    elb_app_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
        'LoadBalancing:Application: APN2-LoadBalancerUsage', 0))
    ##-----------------------------------------------------##

    ## SIMPLE NOTIFICATION SERVICE
    ## from *cost by service* ##
    ## NOTE 2019.02.05: DEV generally doesn't use AWS SNS, so the
    ## key 'Amazon Simple Notification Service' might not appear in
    ## the list of svcs returned by Cost Explorer!
    if 'Amazon Simple Notification Service' not in res_dict.keys():
        res_dict['Amazon Simple Notification Service'] = dict()
        res_dict['Amazon Simple Notification Service']['Cost'] = 0
    sns = Decimal(res_dict['Amazon Simple Notification Service']['Cost'])
    ##-----------------------------------------------------##

    ## TOTAL COST computed from *cost by service*
    total_cost_svc = (ec2_compute + ec2_other + rdb_service +
                      cloudwatch + ecredis + ec2_elb + sns)

    with open(outfile, 'w') as f:
        print("*TOTAL COST in DEV* on %s:\t*$%s*"
              %(rpt_date, total_cost_svc.quantize(Decimal("1.00"))))
        f.write("*TOTAL COST in DEV* on %s:\t*$%s*\n"
                %(rpt_date, total_cost_svc.quantize(Decimal("1.00"))))
        print("==================================================")
        f.write("==================================================\n")
        print("\t`EC2-compute`:\t$%s"
              % ec2_compute.quantize(Decimal("1.000")))
        f.write("\t`EC2-compute`:\t$%s\n"
              % ec2_compute.quantize(Decimal("1.000")))
        print("\t`EC2-other`:\t$%s"
              % ec2_other.quantize(Decimal("1.000")))
        f.write("\t`EC2-other`:\t$%s\n"
              % ec2_other.quantize(Decimal("1.000")))
        print("\t`Cloudwatch`:\t$%s"
              % cloudwatch.quantize(Decimal("1.000")))
        f.write("\t`Cloudwatch`:\t$%s\n"
              % cloudwatch.quantize(Decimal("1.000")))
        print("\t`RDB Service`:\t$%s"
              % rdb_service.quantize(Decimal("1.000")))
        f.write("\t`RDB Service`:\t$%s\n"
              % rdb_service.quantize(Decimal("1.000")))
        print("\t`Elasticache`:\t$%s"
              % ecredis.quantize(Decimal("1.000")))
        f.write("\t`Elasticache`:\t$%s\n"
              % ecredis.quantize(Decimal("1.000")))
        print("\t`EC2 LoadBal`:\t$%s"
              % ec2_elb.quantize(Decimal("1.000")))
        f.write("\t`EC2 LoadBal`:\t$%s\n"
              % ec2_elb.quantize(Decimal("1.000")))
        print("\t`SNS (noti)`:\t$%s"
              % sns.quantize(Decimal("1.000")))
        f.write("\t`SNS (noti)`:\t$%s\n"
              % sns.quantize(Decimal("1.000")))


def send_to_slack(filename, webhook_url, username):
    """
    str, str -> int

    Given a filename (str) and webhook_url (str), send a json
    payload in an http POST request to Slack http endpoint for
    a Slack channel. Returns an http status code (integer)
    """
    with open(filename, 'r') as f:
        results = f.read()

    payload = {
        "username" : username,
        "text" : results
    }

    print("Sending payload to slack channel %s ..." %webhook_url)

    resp = requests.post(
        webhook_url,
        json.dumps(payload),
        headers = {'Content-Type': 'application/json'}
        )

    return resp.status_code


def main():
    # Boilerplate for reading in arguments
    parser = argparse.ArgumentParser(
        description="This program takes a single optional argument "
                    "'--mode' which can be one of 'test' and 'real'. "
                    "Test mode does not send results to Slack.")
    parser.add_argument('--mode', type = str, nargs = '?',
                        default = 'real', const = 'real',
                        help = "optional argument, one of 'test' or 'real'."
                        "'test' only prints results to stdout.")
    args = parser.parse_args()

    # datetime-related vars
    UTC = datetime.datetime.utcnow()
    KST = UTC + datetime.timedelta(days = 9/24)
    EST = KST - datetime.timedelta(days = 1) # EST is UTC - 5
    EST2 = KST - datetime.timedelta(days = 2)
    Tstart = EST2.strftime('%Y-%m-%d')
    Tend = EST.strftime('%Y-%m-%d')
    # output files
    file_path = '/home/ec2-user/bin/'
    ce_general = file_path + 'cost_explorer_daily_dev_' + Tend + '.txt'
    # boto3 session vars
    #session = boto3.Session(profile_name = 'dev')
    session = boto3.Session(profile_name = 'dev_ce_full_ec2_ro')
    ceClient = session.client('ce')
    # Slack 'aws_cost' channel webhook URL
    slack_webhook = 'https://hooks.slack.com/services/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'

    resp_by_service = ceClient.get_cost_and_usage(
        TimePeriod = {
            'Start': Tstart,
            'End': Tend,
        },
        Granularity = 'DAILY',
        Metrics = [
            'UnblendedCost',
        ],
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

    resp_svc_detailed = ceClient.get_cost_and_usage(
        TimePeriod = {
            'Start': Tstart,
            'End': Tend,
        },
        Granularity = 'DAILY',
        Metrics = [
            'UnblendedCost',
        ],
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'OPERATION'
            },
            {
                'Type': 'DIMENSION',
                'Key': 'USAGE_TYPE'
            }
        ]
    )

    svc_results = extract_ce(resp_by_service, resp_svc_detailed)
    #print(svc_results)

    prez_extract_ce(svc_results, Tend, ce_general)

    if args.mode == 'real':
        print("Send non-RI Daily DEV Cost Explorer data to Slack")
        http_status = send_to_slack(ce_general, slack_webhook,
                                    'AWS_Cost_Explorer DEV')
        if http_status != 200:
            print("Sending DEV AWS Cost Explorer data payload to %s FAILED!"
                  % slack_webhook)
        else:
            print("Sending DEV AWS Cost Explorer data payload to %s SUCCESS!"
                  % slack_webhook)


if __name__ == "__main__":
    main()
