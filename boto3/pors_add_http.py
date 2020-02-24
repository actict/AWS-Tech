import boto3

session = boto3.Session(profile_name = 'ops')

ec2Client = session.client('ec2')

req=ec2Client.authorize_security_group_ingress(

        GroupId = 'sg-07434c721bac1ffd7',

        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'IpRanges': [
                   {
                       'CidrIp':'10.0.254.0/23',
                   },
                            ],
                'ToPort': 80,
            },
                     ],
)

print(req)
