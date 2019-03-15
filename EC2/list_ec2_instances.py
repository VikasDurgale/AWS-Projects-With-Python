import boto3

session = boto3.session.Session(profile_name='AWSwithPython')
ec2 = session.resource('ec2')

""" List of all the instances."""
for instance in ec2.instances.all():
    print(instance.instance_id)

""" List of stopped instances.
for instance in ec2.instances.all():
    if instance.state['Name'] == 'stopped':
        print(instance.instance_id)

for instance in ec2.instances.filter(
    Filters=[{
        'Name': 'instance-state-name',
        'Values': ['stopped']
    }]):
    print(instance.instance_id)
"""
