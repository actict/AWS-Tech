#!/usr/bin/env python3
# lib_cloudwatch_alarms.py
#
# Last Updated: 2018.12.14
# Updated by: scott.hwang@peertec.com
#
# This script provides functions for creating regular cloudwatch
# alarms for EC2 status as well as special alarms for collectd
# including cpu, memory, disk, processes, IOPS, etc. If an alarm is
# triggered, it will send a notification to an AWS SNS topic for a
# given EC2 instance. This script assumes that the proper IAM
# permissions allowing 'collectd' and 'cloudwatch_put_metric' have
# been applied to the EC2 instance(s)
#
# This script is not intended to be executed directly, but rather
# should be 'import'ed into other boto3 scripts.


def create_collectd_cpu_alarm(boto3cw, instname, sns, iid):
    """
    boto3 client object, string, string, string -> dict

    Takes a boto3 cloudwatch client object, and 3 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID

    This function returns the result of put_metric_alarm() for a
    CPU alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-CPU-gt-90pct-10min',
        AlarmDescription = 'Alarm if CPU usage gt 90pct for 10 of 10 periods',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 10,
        MetricName = 'cpu.percent.active',
        Namespace = 'collectd',
        Period = 60,
        Statistic = 'Average',
        Threshold = 90.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'Host',
                'Value': iid
            },
            {
                'Name': 'PluginInstance',
                'Value': 'NONE'
            }
        ],
        TreatMissingData = 'missing'
    )
    return resp


def create_collectd_mem_alarm(boto3cw, instname, sns, iid):
    """
    boto3 client object, string, string, string -> dict

    Takes a boto3 cloudwatch client object, and 3 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID

    This function returns the result of put_metric_alarm() for a
    memory alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-memory-gt-80pct-10min',
        AlarmDescription = 'Alarm if memory usage gt 80pct for 10 of 10 periods',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 10,
        MetricName = 'memory.percent.used',
        Namespace = 'collectd',
        Period = 60,
        Statistic = 'Average',
        Threshold = 80.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'Host',
                'Value': iid
            },
            {
                'Name': 'PluginInstance',
                'Value': 'NONE'
            }
        ],
        TreatMissingData = 'missing',
    )
    return resp


def create_collectd_root_disk_alarm(boto3cw, instname, sns, iid):
    """
    boto3 client object, string, string, string -> dict

    Takes a boto3 cloudwatch client object, and 3 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID

    This function returns the result of put_metric_alarm() for a
    disk alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-disk-usage-gt-75pct-10min',
        AlarmDescription = 'Alarm if disk usage gt 75pct for 10 of 10 periods',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 10,
        MetricName = 'df.percent_bytes.used',
        Namespace = 'collectd',
        Period = 60,
        Statistic = 'Average',
        Threshold = 75.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'Host',
                'Value': iid
            },
            {
                'Name': 'PluginInstance',
                'Value': 'root'
            }
        ],
        TreatMissingData = 'missing',
    )
    return resp


def create_collectd_nonroot_disk_alarm(boto3cw, instname, sns, iid, plugin, diskname):
    """
    boto3 client object, string x 5ea -> dict

    Takes a boto3 cloudwatch client object, and 5 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID
    (4) PluginInstance name for collectd (disk name)
        (you can find this from 'Metrics' -> collectd in CW)
    (5) user-specified diskname in cloudwatch alarm

    This function returns the result of put_metric_alarm() for a
    non-root disk alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-' + diskname + '-usage-gt-75pct-10min',
        AlarmDescription = 'Alarm if disk usage gt 75pct for 10 of 10 periods',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 10,
        MetricName = 'df.percent_bytes.used',
        Namespace = 'collectd',
        Period = 60,
        Statistic = 'Average',
        Threshold = 75.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'Host',
                'Value': iid
            },
            {
                'Name': 'PluginInstance',
                'Value': plugin
            }
        ],
        TreatMissingData = 'missing',
    )
    return resp


def create_collectd_process_alarm(boto3cw, instname, sns, iid, plugin):
    """
    boto3 client object, string x 4ea -> dict

    Takes a boto3 cloudwatch client object, and 4 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID
    (4) PluginInstance name for collectd

    This function returns the result of put_metric_alarm() for a
    collectd number of processes alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-' + plugin + '-num-processes',
        AlarmDescription = 'Alarm if number of processes lt 1 for 30 sec',
        ComparisonOperator = 'LessThanThreshold',
        EvaluationPeriods = 3,
        MetricName = 'processes.ps_count.processes',
        Namespace = 'collectd',
        Period = 10,
        Statistic = 'Average',
        Threshold = 1.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'Host',
                'Value': iid
            },
            {
                'Name': 'PluginInstance',
                'Value': plugin
            }
        ],
        TreatMissingData = 'missing',
    )
    return resp


def create_ec2_status_alarm(boto3cw, instname, sns, iid):
    """
    boto3 client object, string, string, string -> dict

    Takes a boto3 cloudwatch client object, and 3 strings:

    (1) Instance Name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) EC2 instance ID

    This function returns the result of put_metric_alarm() for an
    EC2 status failed alarm
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = instname + '-status-failed',
        AlarmDescription = '',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 2,
        MetricName = 'StatusCheckFailed',
        Namespace = 'AWS/EC2',
        Period = 60,
        Statistic = 'Average',
        Threshold = 2,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'InstanceId',
                'Value': iid
            },
        ],
        TreatMissingData = 'missing',
        Unit = 'Count'
    )
    return resp


def create_ebs_iops_alarm(boto3cw, instname, sns, volname):
    """
    """


def create_elastic_beanstalk_health_alarm(boto3cw, envname, sns):
    """
    boto3 cloudwatch client object, string x 2ea -> dict

    Takes a boto3 cloudwatch client object and 2 strings

    (1) Elastic Beanstalk envo name
    (2) Simple Notification Service ARN (for alarm notification)
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = envname + '-EB' + '-envo-health-alarm',
        AlarmDescription = 'Alarm if status "20 degraded" or "25 severe" for 5 of 5 periods',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 5,
        MetricName = 'EnvironmentHealth',
        Namespace = 'AWS/ElasticBeanstalk',
        Period = 60,
        Statistic = 'Maximum',
        Threshold = 20.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'EnvironmentName',
                'Value': envname
            },
        ],
    )


def create_elastic_beanstalk_max_disk_usage_alarm(boto3cw, envname, sns):
    """
    boto3 cloudwatch client object, string x 2ea -> dict

    Takes a boto3 cloudwatch client object and 2 strings

    (1) Elastic Beanstalk envo name
    (2) Simple Notification Service ARN (for alarm notification)
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = envname + '-EB' + '-envo-max-disk-usage-gt-75pct-5min',
        AlarmDescription = 'Alarm if root disk usage in any instance gt 75pct for 5min',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 5,
        MetricName = 'RootFilesystemUtil',
        Namespace = 'AWS/ElasticBeanstalk',
        Period = 60,
        Statistic = 'Maximum',
        Threshold = 75.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'EnvironmentName',
                'Value': envname
            },
        ]
    )


def create_elastic_beanstalk_max_cpu_alarm(boto3cw, envname, sns, asg):
    """
    boto3 cloudwatch client object, string x 3ea -> dict

    Takes a boto3 cloudwatch client object and 2 strings

    (1) Elastic Beanstalk envo name
    (2) Simple Notification Service ARN (for alarm notification)
    (3) Auto Scaling Group
    """
    resp = boto3cw.put_metric_alarm(
        AlarmName = envname + '-EB' + '-envo-max-CPU-usage-gt-90pct-10min',
        AlarmDescription = 'Alarm if CPU usage in any instance gt 90pct for 10 min',
        ComparisonOperator = 'GreaterThanOrEqualToThreshold',
        EvaluationPeriods = 10,
        MetricName = 'CPUUtilization',
        Namespace = 'AWS/EC2',
        Period = 60,
        Statistic = 'Maximum',
        Threshold = 90.0,
        AlarmActions = [sns],
        Dimensions = [
            {
                'Name': 'AutoScalingGroupName',
                'Value': asg
            },
        ]
    )


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
