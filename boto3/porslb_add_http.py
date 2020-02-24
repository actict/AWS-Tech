import boto3

session = boto3.Session(profile_name = 'ops')

ec2Client = session.client('ec2')

req=ec2Client.authorize_security_group_ingress(

        GroupId = 'sg-0bf9d5aa619076b8f',
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'IpRanges': [
                   {
                       'CidrIp':'10.0.254.0/23',
                   },
                            ],
                'ToPort': 443,
            },
                     ],
)

print(req)
