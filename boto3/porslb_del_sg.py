import boto3

session = boto3.Session(profile_name = 'ops')

ec2Client = session.client('ec2')

req=ec2Client.revoke_security_group_ingress(

        GroupId = 'sg-0bf9d5aa619076b8f',
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'UserIdGroupPairs': [{ 'GroupId': 'sg-0aebbff46baba721a' }] }
            ],
        )


print(req)
