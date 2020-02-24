#!/usr/bin/env python3
# daily_cost_report_pecunian.py
#
# Last Updated: 2019.05.23
# Updated by: scott.hwang@peertec.com
#
# This boto3 script uses the AWS Cost Explorer API to query the
# billing data from the previous day for PECUNIAN envo. Extracted data
# includes the following:
# - A. Daily Bill by Service Type
#   + EC2 Instances
#   + EC2 Other
#   + EC2 Load Balancer
#   + Cloudwatch
#   + RDB Service
#   + Elasticache Redis
#   + SNS
# - B. Reserved Instance (RI) Utilization (PECUNIAN, PROD & DEV)
# - C. Detailed line-item breakdown by Service Type (TODO)
#
# Important billing data will be extracted from the JSON results and
# formatted so they can be sent to Slack.


import argparse
import boto3
import datetime
from decimal import Decimal
import json
import requests
import time


def extract_ce(svc_dict, utype_dict):
    """
    dict, dict -> dict

    Given 'svc_dict', a nested dict of lists containing Cost Explorer
    (CE) data grouped by Service and 'utype_dict', a nested dict of
    lists containing CE data grouped by both Operation and Usage_Type,
    return a dict containing all non-RI CE billing data for 'EC2',
    'EC2-Other', 'Load Balancer', 'Cloudwatch', 'RDB', 'Elasticache',
    'S3', and line items for each service.
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
         'RunInstances: APN2-BoxUsage:t2.large',
         'RunInstances: APN2-BoxUsage:t2.medium',
         'RunInstances: APN2-BoxUsage:t2.micro',
         'RunInstances: APN2-BoxUsage:t2.nano',
         'RunInstances: APN2-BoxUsage:t2.small',
         'RunInstances: APN2-BoxUsage:t3.large',
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


def extract_ce_RI(ri_dict):
    """
    dict -> dictOfDicts

    Given 'ri_dict', a nested dict of lists containing Cost Explorer
    (CE) data grouped by Subscription_Id for Reserved Instances data,
    return a dict of dicts containing RI CE billing data such as RI
    utilization (%) and number of instances for each RI type.
    """
    res = dict()
    lod = ri_dict['UtilizationsByTime'][0]['Groups']
    #print("length of ri_dict is: %d" % len(lod))
    utcnow = datetime.datetime.utcnow()
    for i in range(len(lod)):
        d0 = lod[i]['Attributes']
        d1 = lod[i]['Utilization']

        #print("dict %d: %s" %(i, d0))

        # create custom key that is a combination of 'instanceType'
        # and 'offeringType' key values
        instType = d0['instanceType']
        contractType = d0['offeringType']
        customKey = instType + '-' + contractType

        # Check RI contract 'endDate' and 'cancellationDate'
        ri_end_date_str = d0['endDateTime']
        ri_cancel_date_str = d0['cancellationDateTime']
        ri_end_datetime_obj = datetime.datetime.strptime(
            ri_end_date_str[0:10], '%Y-%m-%d')
        ri_cancel_datetime_obj = datetime.datetime.strptime(
            ri_cancel_date_str[0:10], '%Y-%m-%d')

        #print("customKey: %s" % customKey)
        #print("ri_cancel_datetime_obj is %s" %ri_cancel_datetime_obj)
        #print("ri_end_datetime_obj is %s" %ri_cancel_datetime_obj)

        # Only add RI data to dict if the RI cancel/end date g.t.
        # today's UTC date
        if ri_end_datetime_obj > utcnow:
            # check if the key already exists or not to avoid overwriting
            # existing key-keyval pair
            if customKey not in res:
                #print("Create key %s with init'ed dict as keyval" % customKey)
                res[customKey] = {
                    'numberOfInstances': Decimal(0),
                    'UtilizationPercentage': Decimal(0),
                }

            #print("Add key and keyval for 'numberOfInstances' for %s"
            #      %d0['instanceType'])
            res[customKey]['numberOfInstances'] += Decimal(
                d0['numberOfInstances'])

            #print("Add key and keyval for 'UtilizationPercentage' for %s"
            #      %d0['instanceType'])
            # Note: in the case of duplicated 'customKey's, the logic
            # below will only reflect keyvals from the 2nd instance of
            # 'customKey'.
            # TODO: to properly calculate 'UtilizationPercentage', you
            # need to calculate exactly how many RI's are being used per
            # type and sum over all used instances and then calculate a
            # consolidated 'UtilizationPercentage'. For now, I'm not
            # going to do this. 2019.01.24
            res[customKey]['UtilizationPercentage'] = Decimal(d1[
                'UtilizationPercentage'])

    return res


# TODO: rewrite the function below and other functions so that
# they take an object of type 'CostExplorerClient' instead of a
# regular dict. This will allow me to remove cost explorer
# filter/queries from main() and place them within specific
# functions themselves. This has the benefit of enabling code
# reuse if this program is imported from other scripts.
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
    ec2_compute_t2_large = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t2.large', 0))
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
    ec2_compute_t3_large = Decimal(res_dict[
        'Amazon Elastic Compute Cloud - Compute'].get(
            'RunInstances: APN2-BoxUsage:t3.large', 0))
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
    rdb_service = Decimal(res_dict.get(
        'Amazon Relational Database Service', 0))
    ##-----------------------------------------------------##
    ## from *cost by utilization type* ##
    rdb_aurora_storage_io = Decimal(res_dict.get(
        'Amazon Relational Database Service', 0))
    rdb_aurora_storage_usage = Decimal(res_dict.get(
        'Amazon Relational Database Service', 0))
    rdb_instance_usage_db_r4_xlarge = Decimal(res_dict.get(
        'Amazon Relational Database Service', 0))

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

    # ## ELASTICACHE
    # ## from *cost by service* ##
    # ecredis = Decimal(res_dict['Amazon ElastiCache']['Cost'])
    # ##-----------------------------------------------------##
    # ## *from cost by utilization type* ##
    # ecredis_cache_m4_xlarge = Decimal(res_dict['Amazon ElastiCache'].get(
    #     'CreateCacheCluster:0002: APN2-NodeUsage:cache.m4.xlarge', 0))
    # ##-----------------------------------------------------##

    # ## ELASTIC LOAD BALANCER
    # ## from *cost by service* ##
    # ec2_elb = Decimal(res_dict['Amazon Elastic Load Balancing']['Cost'])
    # ##-----------------------------------------------------##
    # ## from *cost by utilization type*
    # elb_data_processing_bytes = Decimal(res_dict[
    #     'Amazon Elastic Load Balancing'].get(
    #         'LoadBalancing: APN2-DataProcessing-Bytes', 0))
    # elb_egress_bytes = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
    #     'LoadBalancing: APN2-DataTransfer-Out-Bytes', 0))
    # elb_egress_regional_bytes = Decimal(res_dict[
    #     'Amazon Elastic Load Balancing'].get(
    #         'LoadBalancing-PublicIP-Out: APN2-DataTransfer-Regional-Bytes', 0))
    # elb_lcu_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
    #     'LoadBalancing:Application: APN2-LCUUsage', 0))
    # elb_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
    #     'LoadBalancing: APN2-LoadBalancerUsage', 0))
    # elb_app_usage = Decimal(res_dict['Amazon Elastic Load Balancing'].get(
    #     'LoadBalancing:Application: APN2-LoadBalancerUsage', 0))
    # ##-----------------------------------------------------##

    # ## SIMPLE NOTIFICATION SERVICE
    # ## from *cost by service* ##
    # sns = Decimal(res_dict['Amazon Simple Notification Service']['Cost'])
    # ##-----------------------------------------------------##

    ## TOTAL COST computed from *cost by service*
#    total_cost_svc = (ec2_compute + ec2_other + rdb_service +
#                      cloudwatch + ecredis + ec2_elb + sns)
    total_cost_svc = ec2_compute + ec2_other + cloudwatch

    with open(outfile, 'w') as f:
        print("*TOTAL COST in PECUNIAN* on %s:\t*$%s*"
              %(rpt_date, total_cost_svc.quantize(Decimal("1.00"))))
        f.write("*TOTAL COST in PECUNIAN* on %s:\t*$%s*\n"
                %(rpt_date, total_cost_svc.quantize(Decimal("1.00"))))
        print("==================================================")
        f.write("==================================================\n")
        print("\t`EC2-compute`:\t$%s"
              % ec2_compute.quantize(Decimal("1.000")))
        f.write("\t`EC2-compute`:\t$%s\n"
              % ec2_compute.quantize(Decimal("1.000")))

        # print("\t\t`RunInstances: APN2-BoxUsage:t2.nano`:\t$%s"
        #       % ec2_compute_t2_nano.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t2.nano`:\t$%s\n"
        #       % ec2_compute_t2_nano.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t2.micro`:\t$%s"
        #       % ec2_compute_t2_micro.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t2.micro`:\t$%s\n"
        #       % ec2_compute_t2_micro.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t2.small`:\t$%s"
        #       % ec2_compute_t2_small.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t2.small`:\t$%s\n"
        #       % ec2_compute_t2_small.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t2.medium`:\t$%s"
        #       % ec2_compute_t2_medium.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t2.medium`:\t$%s\n"
        #       % ec2_compute_t2_medium.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t2.large`:\t$%s"
        #       % ec2_compute_t2_large.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t2.large`:\t$%s\n"
        #       % ec2_compute_t2_large.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t3.nano`:\t$%s"
        #       % ec2_compute_t3_nano.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t3.nano`:\t$%s\n"
        #       % ec2_compute_t3_nano.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t3.micro`:\t$%s"
        #       % ec2_compute_t3_micro.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t3.micro`:\t$%s\n"
        #       % ec2_compute_t3_micro.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t3.small`:\t$%s"
        #       % ec2_compute_t3_small.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t3.small`:\t$%s\n"
        #       % ec2_compute_t3_small.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t3.medium`:\t$%s"
        #       % ec2_compute_t3_medium.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t3.medium`:\t$%s\n"
        #       % ec2_compute_t3_medium.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:t3.large`:\t$%s"
        #       % ec2_compute_t3_large.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:t3.large`:\t$%s\n"
        #       % ec2_compute_t3_large.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:m4.large`:\t$%s"
        #       % ec2_compute_m4_large_mswin.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:m4.large`:\t$%s\n"
        #       % ec2_compute_m4_large_mswin.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:m5.large`:\t$%s"
        #       % ec2_compute_m5_large.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:m5.large`:\t$%s\n"
        #       % ec2_compute_m5_large.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:m5.xlarge`:\t$%s"
        #       % ec2_compute_m5_xlarge.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:m5.xlarge`:\t$%s\n"
        #       % ec2_compute_m5_xlarge.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:c5.large`:\t$%s"
        #       % ec2_compute_c5_large.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:c5.large`:\t$%s\n"
        #       % ec2_compute_c5_large.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-BoxUsage:c5.large`:\t$%s"
        #       % ec2_compute_c5_large.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-BoxUsage:c5.large`:\t$%s\n"
        #       % ec2_compute_c5_large.quantize(Decimal("1.000")))
        # print("\t\t`RunInstances: APN2-DataTransfer-Out-Bytes`:\t$%s"
        #       % ec2_compute_egress_data.quantize(Decimal("1.000")))
        # f.write("\t\t`RunInstances: APN2-DataTransfer-Out-Bytes`:\t$%s\n"
        #       % ec2_compute_egress_data.quantize(Decimal("1.000")))
        ##-----------------------------------------------------##
        print("\t`EC2-other`:\t$%s"
              % ec2_other.quantize(Decimal("1.000")))
        f.write("\t`EC2-other`:\t$%s\n"
              % ec2_other.quantize(Decimal("1.000")))
        ##-----------------------------------------------------##
        print("\t`Cloudwatch`:\t$%s"
              % cloudwatch.quantize(Decimal("1.000")))
        f.write("\t`Cloudwatch`:\t$%s\n"
              % cloudwatch.quantize(Decimal("1.000")))
        print("\t`RDB Service`:\t$%s"
              % rdb_service.quantize(Decimal("1.000")))
        # f.write("\t`RDB Service`:\t$%s\n"
        #       % rdb_service.quantize(Decimal("1.000")))
        # print("\t`Elasticache`:\t$%s"
        #       % ecredis.quantize(Decimal("1.000")))
        # f.write("\t`Elasticache`:\t$%s\n"
        #       % ecredis.quantize(Decimal("1.000")))
        # print("\t`EC2 LoadBal`:\t$%s"
        #       % ec2_elb.quantize(Decimal("1.000")))
        # f.write("\t`EC2 LoadBal`:\t$%s\n"
        #       % ec2_elb.quantize(Decimal("1.000")))
        # print("\t`SNS (noti)`:\t$%s"
        #       % sns.quantize(Decimal("1.000")))
        # f.write("\t`SNS (noti)`:\t$%s\n"
        #       % sns.quantize(Decimal("1.000")))


def prez_extract_ce_RI(ri_dict, rpt_date, outfile):
    """
    dictOfDict, str, str -> text to stdout, file

    'ri_dict' contains Reserved Instance (RI) utilization percentage
    by instance type as well as the number of instances
    reserved. 'rpt_date' is a date in YYYY-MM-DD format converted to
    str type from datetime type. This function returns text to stdout
    and writes the same info to file with filename denoted by str var
    'outfile'.
    """
    ri_typesL = ['m5.large-Standard', 'c5.large-Standard',
                 'm4.large-Standard', 't2.nano-Convertible',
                 't2.nano-Standard', 't3.nano-Convertible',
                 't3.nano-Standard']

    for ri_type in ri_typesL:
        if ri_type in ri_dict.keys():
            if ri_type == 'm5.large-Standard':
                m5_large_ri_std_usage_pct = Decimal(
                    ri_dict['m5.large-Standard']['UtilizationPercentage'])
                m5_large_ri_std_num_inst = Decimal(
                    ri_dict['m5.large-Standard']['numberOfInstances'])
            elif ri_type == 'c5.large-Standard':
                c5_large_ri_std_usage_pct = Decimal(
                    ri_dict['c5.large-Standard']['UtilizationPercentage'])
                c5_large_ri_std_num_inst = Decimal(
                    ri_dict['c5.large-Standard']['numberOfInstances'])
            elif ri_type == 'm4.large-Standard':
                m4_large_ri_std_usage_pct = Decimal(
                    ri_dict['m4.large-Standard']['UtilizationPercentage'])
                m4_large_ri_std_num_inst = Decimal(
                    ri_dict['m4.large-Standard']['numberOfInstances'])
            elif ri_type == 't2.nano-Convertible':
               t2_nano_ri_conv_usage_pct = Decimal(
                   ri_dict['t2.nano-Convertible']['UtilizationPercentage'])
               t2_nano_ri_conv_num_inst = Decimal(
                   ri_dict['t2.nano-Convertible']['numberOfInstances'])
            elif ri_type == 't2.nano-Standard':
                t2_nano_ri_std_usage_pct = Decimal(
                    ri_dict['t2.nano-Standard']['UtilizationPercentage'])
                t2_nano_ri_std_num_inst = Decimal(
                    ri_dict['t2.nano-Standard']['numberOfInstances'])
            elif ri_type == 't3.nano-Convertible':
                t3_nano_ri_conv_usage_pct = Decimal(
                    ri_dict['t3.nano-Convertible']['UtilizationPercentage'])
                t3_nano_ri_conv_num_inst = Decimal(
                    ri_dict['t3.nano-Convertible']['numberOfInstances'])
            elif ri_type == 't3.nano-Standard':
                t3_nano_ri_std_usage_pct = Decimal(
                    ri_dict['t3.nano-Standard']['UtilizationPercentage'])
                t3_nano_ri_std_num_inst = Decimal(
                    ri_dict['t3.nano-Standard']['numberOfInstances'])
        else:  # if key 'ri_type' is not found in 'ri_dict', set vals to 0
            if ri_type == 'm5.large-Standard':
                m5_large_ri_std_usage_pct = Decimal(0)
                m5_large_ri_std_num_inst = Decimal(0)
            elif ri_type == 'c5.large-Standard':
                c5_large_ri_std_usage_pct = Decimal(0)
                c5_large_ri_std_num_inst = Decimal(0)
            elif ri_type == 'm4.large-Standard':
                m4_large_ri_std_usage_pct = Decimal(0)
                m4_large_ri_std_num_inst = Decimal(0)
            elif ri_type == 't2.nano-Convertible':
                t2_nano_ri_conv_usage_pct = Decimal(0)
                t2_nano_ri_conv_num_inst = Decimal(0)
            elif ri_type == 't3.nano-Convertible':
                t3_nano_ri_conv_usage_pct = Decimal(0)
                t3_nano_ri_conv_num_inst = Decimal(0)
            elif ri_type == 't3.nano-Standard':
                t3_nano_ri_std_usage_pct = Decimal(0)
                t3_nano_ri_std_num_inst = Decimal(0)

    with open(outfile, 'w') as f:
        print("*PECUNIAN RI USAGE DATA* on %s" % rpt_date)
        f.write("*PECUNIAN RI USAGE DATA* on %s\n" % rpt_date)
        print("============================================")
        f.write("============================================\n")
        print("\t`t2.nano RI Convertible %% used`:\t%s%%"
              % t2_nano_ri_conv_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`t2.nano RI Convertible %% used`:\t%s%%\n"
                % t2_nano_ri_conv_usage_pct.quantize(Decimal("1.00")))
        print("\t`t2.nano RI Convertible 수량`:\t\t%s"
              % t2_nano_ri_conv_num_inst)
        f.write("\t`t2.nano RI Convertible 수량`:\t\t\t%s\n"
                % t2_nano_ri_conv_num_inst)
        ##-----------------------------------------------------##
        print("\t`t2.nano RI Standard %% used`:\t\t%s%%"
              % t2_nano_ri_std_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`t2.nano RI Standard %% used`:\t\t%s%%\n"
                % t2_nano_ri_std_usage_pct.quantize(Decimal("1.00")))
        print("\t`t2.nano RI Standard 수량`:\t\t%s"
              % t2_nano_ri_std_num_inst)
        f.write("\t`t2.nano RI Standard 수량`:\t\t\t%s\n"
                % t2_nano_ri_std_num_inst)
        ##-----------------------------------------------------##
        print("\t`t3.nano RI Convertible %% used`:\t%s%%"
               % t3_nano_ri_conv_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`t3.nano RI Convertible %% used`:\t%s%%\n"
               % t3_nano_ri_conv_usage_pct.quantize(Decimal("1.00")))
        print("\t`t3.nano RI Convertible 수량`:\t\t%s"
              % t3_nano_ri_conv_num_inst)
        f.write("\t`t3.nano RI Convertible 수량`:\t\t\t%s\n"
                % t3_nano_ri_conv_num_inst)
        ##-----------------------------------------------------##
        print("\t`t3.nano RI Standard %% used`:\t\t%s%%"
               % t3_nano_ri_std_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`t3.nano RI Standard %% used`:\t\t%s%%\n"
               % t3_nano_ri_std_usage_pct.quantize(Decimal("1.00")))
        print("\t`t3.nano RI Standard 수량`:\t\t%s"
              % t3_nano_ri_std_num_inst)
        f.write("\t`t3.nano RI Standard 수량`:\t\t\t%s\n"
                % t3_nano_ri_std_num_inst)
        ##-----------------------------------------------------##
        print("\t`m5.large RI Standard %% used`:\t\t%s%%"
              % m5_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`m5.large RI Standard %% used`:\t\t%s%%\n"
                % m5_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        print("\t`m5.large RI Standard 수량`:\t\t%s"
              % m5_large_ri_std_num_inst)
        f.write("\t`m5.large RI Standard 수량`:\t\t\t%s\n"
                % m5_large_ri_std_num_inst)
        ##-----------------------------------------------------##
        print("\t`c5.large RI Standard %% used`:\t\t%s%%"
              % c5_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`c5.large RI Standard %% used`:\t\t%s%%\n"
                % c5_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        print("\t`c5.large RI Standard 수량`:\t\t%s"
              % c5_large_ri_std_num_inst)
        f.write("\t`c5.large RI Standard 수량`:\t\t\t%s\n"
                % c5_large_ri_std_num_inst)
        ##-----------------------------------------------------##
        print("\t`m4.large RI Standard %% used`:\t\t%s%%"
              % m4_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        f.write("\t`m4.large RI Standard %% used`:\t\t%s%%\n"
                % m4_large_ri_std_usage_pct.quantize(Decimal("1.00")))
        print("\t`m4.large RI Standard 수량`:\t\t%s"
              % m4_large_ri_std_num_inst)
        f.write("\t`m4.large RI Standard 수량`:\t\t\t%s\n"
                % m4_large_ri_std_num_inst)


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


def prez_RI_vs_ec2_units(ri_dict, ec2_dict, rpt_date, outfile):
    """
    dict, dict, str, str -> stdout, file

    'ri_dict' contains RI utilization % and RI count for each RI
    contract type.

    'ec2_dict' contains the converted unit count for each ec2
    instance type that GDAC uses across AWS PROD and AWS DEV

    'rpt_date' is a date string in YYYY-MM-DD format converted
    from type 'datetime'.

    This function prints the number of used ec2 base units per type
    alongside the number of contracted ec2 RI units per type. i.e.,

    t2.nano units 사용: 120    t2.nano RI units 구매: 118
    t3.nano units 사용: 286    t3.nano RI units 구매: 326
    ...
    """
    # Combine RI convertible + standard counts for each instance
    # type
    ri_t2_tot_count = (
        ri_dict['t2.nano-Standard']['numberOfInstances']
        )
    ri_t3_tot_count = (
        ri_dict['t3.nano-Standard']['numberOfInstances']
        )
#    ri_m4_tot_count = (
#        ri_dict['m4.large-Standard']['numberOfInstances']
#        )
#    ri_m5_tot_count = (
#        ri_dict['m5.large-Standard']['numberOfInstances']
#        )
#    ri_c5_tot_count = (
#        ri_dict['c5.large-Standard']['numberOfInstances']
#        )

    # Calculate the number of RI units used from utilization %
    # and RI numOfInstances data
    ri_t2_used_count = (
        ri_dict['t2.nano-Standard']['numberOfInstances'] *
        ri_dict['t2.nano-Standard']['UtilizationPercentage']/100
        )
    ri_t3_used_count = (
        ri_dict['t3.nano-Standard']['numberOfInstances'] *
        ri_dict['t3.nano-Standard']['UtilizationPercentage']/100
        )
#    ri_m4_used_count = (
#        ri_dict['m4.large-Standard']['numberOfInstances'] *
#        ri_dict['m4.large-Standard']['UtilizationPercentage']/100
#        )
#    ri_m5_used_count = (
#        ri_dict['m5.large-Standard']['numberOfInstances'] *
#        ri_dict['m5.large-Standard']['UtilizationPercentage']/100
#        )
#    ri_c5_used_count = (
#        ri_dict['c5.large-Standard']['numberOfInstances'] *
#        ri_dict['c5.large-Standard']['UtilizationPercentage']/100
#        )

    with open(outfile, 'w') as f:
        print("*EC2 USED vs RI USED PECUNIAN* on %s" % rpt_date)
        f.write("*EC2 USED vs RI USED PECUNIAN* on %s\n" % rpt_date)
        print("=============================================")
        f.write("=============================================\n")
        print("`t2.nano EC2 used`: %d"
              "\t`t2.nano RI used/total`: %.2f/%d"
              %(ec2_dict['t2.nano'], ri_t2_used_count, ri_t2_tot_count))
        f.write("`t2.nano EC2 used`: %d" %ec2_dict['t2.nano'])
        f.write("\t`t2.nano RI used/total`: %.2f/%d\n"
                %(ri_t2_used_count, ri_t2_tot_count))
        print("`t3.nano EC2 used`: %d"
              "\t`t3.nano RI used/total`: %.2f/%d"
              %(ec2_dict['t3.nano'], ri_t3_used_count, ri_t3_tot_count))
        f.write("`t3.nano EC2 used`: %d" %ec2_dict['t3.nano'])
        f.write("\t`t3.nano RI used/total`: %.2f/%d\n"
                %(ri_t3_used_count, ri_t3_tot_count))
        # print("`m4.large EC2 used`: %d"
        #       "\t`m4.large RI used/total`: %.2f/%d"
        #       %(ec2_dict['m4.large'], ri_m4_used_count, ri_m4_tot_count))
        # f.write("`m4.large EC2 used`: %d" %ec2_dict['m4.large'])
        # f.write("\t`m4.large RI used/total`: %.2f/%d\n"
        #         %(ri_m4_used_count, ri_m4_tot_count))
        # print("`m5.large EC2 used`: %d"
        #       "\t`m5.large RI used/total`: %.2f/%d"
        #       %(ec2_dict['m5.large'], ri_m5_used_count, ri_m5_tot_count))
        # f.write("`m5.large EC2 used`: %d" %ec2_dict['m5.large'])
        # f.write("\t`m5.large RI used/total`: %.2f/%d\n"
        #         %(ri_m5_used_count, ri_m5_tot_count))
        # print("`c5.large EC2 used`: %d"
        #       "\t`c5.large RI used/total`: %.2f/%d"
        #       %(ec2_dict['c5.large'], ri_c5_used_count, ri_c5_tot_count))
        # f.write("`c5.large EC2 used`: %d" %ec2_dict['c5.large'])
        # f.write("\t`c5.large RI used/total`: %.2f/%d\n"
        #         %(ri_c5_used_count, ri_c5_tot_count))


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
    KST = UTC + datetime.timedelta(days = 9/24) # KST is UTC + 9
    EST = KST - datetime.timedelta(days = 1)
    EST2 = KST - datetime.timedelta(days = 2)
    #EST3 = KST - datetime.timedelta(days = 3)
    Tstart = EST2.strftime('%Y-%m-%d')
    Tend = EST.strftime('%Y-%m-%d')
    #Tstart_RI = EST3.strftime('%Y-%m-%d')
    #Tend_RI = EST2.strftime('%Y-%m-%d')

    ### output files ###
    file_path = '/home/ec2-user/bin/'
    f_genl_cost = file_path + 'cost_explorer_daily_pecunian_' + Tend + '.txt'
    f_RI_data = file_path + 'cost_explorer_RI_daily_pecunian_' + Tend + '.txt'
    f_ec2_vs_RI = (
        file_path + 'ec2_unit_count_vs_RI_count_pecunian_'
        + Tend + '.txt')
    ### ------------ ###

    # boto3 session vars
    session = boto3.Session(profile_name = 'pecun_ce_full_ec2_ro')
    ceClient = session.client('ce')
    # boto3 resource object for AWS PECUNIAN
    ec2Resource = session.resource('ec2')
    # dict with key = 'instanceType', keyval = 'instanceCount' in
    # AWS PECUNIAN. Input for prez_RI_vs_ec2_units() !!
    ec2_units_pecun = extract_ec2_units(ec2Resource)

    # Slack 'aws_cost' channel webhook URL
    slack_webhook = 'https://hooks.slack.com/services/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'


    #print("RI dict raw: %s" % ri_info_dict)

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
    # EC2 instances basic unit count

    prez_extract_ce(svc_results, Tend, f_genl_cost)

    #-------------------------------------------------------
    # To avoid AWS Cost Explorer API rate limit, sleep for 1s
    # before querying RI utilization
    time.sleep(1)
    resp_RI_usage_pct = ceClient.get_reservation_utilization(
        TimePeriod = {
            'Start': Tstart,
            'End': Tend,
        },
        GroupBy = [
            {
                'Type': 'DIMENSION',
                'Key': 'SUBSCRIPTION_ID'
            },
        ]
    )

    ### INPUT FOR prez_RI_vs_ec2_units()! ###
    ri_info_dict = extract_ce_RI(resp_RI_usage_pct)
    ### --------------------------------- ###

    # present the raw data from 'ri_info_dict' via markdown-formatted
    # text and pretty-printed on stdout
    prez_extract_ce_RI(ri_info_dict, Tend, f_RI_data)

    # present raw data from 'ri_info_dict', 'ec2_prod_dev_total'
    # side-by-side so you can compare current ec2 usage vs. ec2 RI
    # purchased
    prez_RI_vs_ec2_units(ri_info_dict, ec2_units_pecun, Tend,
                         f_ec2_vs_RI)

    if args.mode == 'real':
        print("Send non-RI Daily Cost Explorer data to Slack")
        http_status = send_to_slack(f_genl_cost, slack_webhook,
                                    'AWS_Cost_Explorer PECUNIAN')
        if http_status != 200:
            print("Sending AWS Cost Explorer data payload to %s FAILED!"
                  % slack_webhook)
        else:
            print("Sending AWS Cost Explorer data payload to %s SUCCESS!"
                  % slack_webhook)
    ##-----------------------------------------------------##
    if args.mode == 'real':
        print("Send RI Cost Explorer data to Slack")
        http_status = send_to_slack(f_RI_data, slack_webhook,
                                    'AWS_RI_Info PECUNIAN')
        if http_status != 200:
            print("Sending AWS RI usage data payload to %s FAILED!"
                  % slack_webhook)
        else:
            print("Sending AWS RI usage data payload to %s SUCCESS!"
                  % slack_webhook)
    ##-----------------------------------------------------##
    if args.mode == 'real':
        print("Send EC2 used vs RI used/count data to Slack")
        http_status = send_to_slack(f_ec2_vs_RI, slack_webhook,
                                    'AWS_RI_Info PECUNIAN')
        if http_status != 200:
            print("Sending EC2 used vs RI data payload to %s FAILED!"
                  % slack_webhook)
        else:
            print("Sending EC2 used vs RI data payload to %s SUCCESS!"
                  % slack_webhook)


if __name__ == "__main__":
    main()
