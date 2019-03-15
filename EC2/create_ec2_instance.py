import boto3

session = boto3.session.Session(profile_name='AWSwithPython')
ec2 = session.resource('ec2')
