#!/bin/bash
# cloudtrail_errors.sh
#
# Last Updated: 2018.12.13
# Updated by: scott.hwang@peertec.com
#
# This script calls 'get_cloudwatch_logs.py' and runs a query against
# AWS Cloudwatch Logs to find all cloudtrail error events. If results
# exist, they will be sent to the slack channel
# 'notify_cloudtrail'. This script is intended to be run at regular
# intervals by a cron script or systemd timer (preferred).


appfolder="/home/ec2-user/bin"
### args for get_cloudwatch_logs.py ###

# filterp, resultf, mailsubj for 'cloudtrail auth failure'
awsenvo='prod_cw_logs_ro'
log_grp="actwo_cloudtrail"
filterp='{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }'
t_start=$(date -u +%F' '%H:%M:%S --date '-420 sec')
t_end=$(date -u +%F' '%H:%M:%S --date '-60 sec')
resultf="$appfolder/cloudtrail_authfail"
logfile="$appfolder/get_cw_logs_cloudtrail.log"
### args for smtp-cli ###
slack_email="s3w6l4c4f0x8f9w4@whalex.slack.com"
mailhost="smtp.gmail.com"
mailuser="admin@actwo.com"
mailpw="$(<"$appfolder"/gmail_pass.txt)"
mailsubj="Cloudtrail Authorization Failure!"


# check for python3
if [ -f /usr/bin/python3 ]; then
  :
else
  printf "%s\\n" "### python3 not installed! Install it and try again ###"
  exit 1
fi

# check for smtp-cli in $appfolder
if [ -f "$appfolder"/smtp-cli ]; then
  :
else
  printf "%s\\n" "### smtp-cli not installed! Install it and try again ###"
  exit 1
fi

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8
else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 2nd filterp, resultf and mailsubj for 'cloudtrail changes'
filterp='{ ($.eventName = CreateTrail) || ($.eventName = UpdateTrail) || ($.eventName = DeleteTrail) || ($.eventName = StartLogging) || ($.eventName = StopLogging) }'
resultf="$appfolder/cloudtrail_changes"
mailsubj="Cloudtrail Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 3rd filter pattern, resultf, and mailsubj for
# 'Console SignIn Failure'
filterp='{ ($.eventName = ConsoleLogin) && ($.errorMessage = "Failed authentication") }'
resultf="$appfolder/cloudtrail_console_signin_failure"
mailsubj="Cloudtrail Console Sign-In Failure!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 4th filter pattern, resultf, and mailsubj for
# 'EC2 Instance Changes' (start, reboot, stop, terminate)
filterp='{ ($.eventName = RunInstances) || ($.eventName = RebootInstances) || ($.eventName = StartInstances) || ($.eventName = StopInstances) || ($.eventName = TerminateInstances) }'
resultf="$appfolder/cloudtrail_ec2_instance_changes"
mailsubj="Cloudtrail EC2 Instance Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 5th filter pattern, resultf, and mailsubj for
# 'EC2 Large Instance Changes' ( *.8xlarge, *.4xlarge)
filterp='{ ($.eventName = RunInstances) && (($.requestParameters.instanceType = *.8xlarge) || ($.requestParameters.instanceType = *.4xlarge)) }'
resultf="$appfolder/cloudtrail_ec2_large_instance_changes"
mailsubj="Cloudtrail EC2 Large Instance Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 6th filter pattern, resultf, and mailsubj for
# 'Internet Gateway Changes'
filterp='{ ($.eventName = CreateCustomerGateway) || ($.eventName = DeleteCustomerGateway) || ($.eventName = AttachInternetGateway) || ($.eventName = CreateInternetGateway) || ($.eventName = DeleteInternetGateway) || ($.eventName = DetachInternetGateway) }'
resultf="$appfolder/cloudtrail_IGW_changes"
mailsubj="Cloudtrail Internet Gateway Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 7th filter pattern, resultf, and mailsubj for
# 'IAM Policy Changes'
filterp='{($.eventName=DeleteGroupPolicy)||($.eventName=DeleteRolePolicy)||($.eventName=DeleteUserPolicy)||($.eventName=PutGroupPolicy)||($.eventName=PutRolePolicy)||($.eventName=PutUserPolicy)||($.eventName=CreatePolicy)||($.eventName=DeletePolicy)||($.eventName=CreatePolicyVersion)||($.eventName=DeletePolicyVersion)||($.eventName=AttachRolePolicy)||($.eventName=DetachRolePolicy)||($.eventName=AttachUserPolicy)||($.eventName=DetachUserPolicy)||($.eventName=AttachGroupPolicy)||($.eventName=DetachGroupPolicy)}'
resultf="$appfolder/cloudtrail_IAM_policy_changes"
mailsubj="Cloudtrail IAM Policy Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 8th filter pattern, resultf, and mailsubj for
# 'Network ACL Changes'
filterp='{ ($.eventName = CreateNetworkAcl) || ($.eventName = CreateNetworkAclEntry) || ($.eventName = DeleteNetworkAcl) || ($.eventName = DeleteNetworkAclEntry) || ($.eventName = ReplaceNetworkAclEntry) || ($.eventName = ReplaceNetworkAclAssociation) }'
resultf="$appfolder/cloudtrail_network_ACL_changes"
mailsubj="Cloudtrail Network ACL Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

sleep 1

# Define 9th filter pattern, resultf, and mailsubj for
# 'Security Group Changes'
filterp='{ ($.eventName = AuthorizeSecurityGroupIngress) || ($.eventName = AuthorizeSecurityGroupEgress) || ($.eventName = RevokeSecurityGroupIngress) || ($.eventName = RevokeSecurityGroupEgress) || ($.eventName = CreateSecurityGroup) || ($.eventName = DeleteSecurityGroup) }'
resultf="$appfolder/cloudtrail_security_group_changes"
mailsubj="Cloudtrail Security Group Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi

# Define 10th filter pattern, resultf, and mailsubj for
# 'VPC Changes'
filterp='{ ($.eventName = CreateVpc) || ($.eventName = DeleteVpc) || ($.eventName = ModifyVpcAttribute) || ($.eventName = AcceptVpcPeeringConnection) || ($.eventName = CreateVpcPeeringConnection) || ($.eventName = DeleteVpcPeeringConnection) || ($.eventName = RejectVpcPeeringConnection) || ($.eventName = AttachClassicLinkVpc) || ($.eventName = DetachClassicLinkVpc) || ($.eventName = DisableVpcClassicLink) || ($.eventName = EnableVpcClassicLink) }'
resultf="$appfolder/cloudtrail_VPC_changes"
mailsubj="Cloudtrail VPC Changes!"

python3 "$appfolder"/get_cloudwatch_logs.py "$awsenvo" "$log_grp" \
        "$filterp" "$t_start" "$t_end" "$resultf" "$logfile"

if [ -s "$resultf" ]; then
  printf "%s\\n" "### Sending $resultf email to $slack_email"
  "$appfolder"/smtp-cli --verbose --host=$mailhost --enable-auth \
                      --user=$mailuser --pass="$mailpw" --from=$mailuser \
                      --to=$slack_email  --subject="$mailsubj" \
                      --body-plain="$resultf" --charset=UTF-8

else
  printf "%s\\n" "### No $resultf to send right now ###"
fi
x
