#!/usr/bin/python

# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError


class EC2Manager:
    """Manage EC2 Instances."""

    def __init__(self, session):
        """Create a EC2Manager object."""
        self.session = session
        self.ec2 = self.session.resource('ec2')

    def list_instances(self):
    	"""List all the EC2 instances created"""
    	for instance in self.ec2.instances.all():
            name = None
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    name = tag['Value']
            print("Id: "+ instance.id +", Name: "+ name +", State: "+ instance.state['Name'])

    def create_tag(self, resource_id, data):
        """Create's Tag for your EC2 instance."""
        tags=list()
        for item in data.items():
            tag_item=dict()
            tag_item['Key'] = item[0]
            tag_item['Value'] = item[1]
            tags.append(tag_item)
        self.ec2.create_tags(
            Resources=[resource_id],
            Tags=tags
        )

    def find_ami_id(self, ami_id, region):
        """Find AMI ID from different region AMI ID."""
        try:
            if self.session.region_name != region:
                self.ec2_or = self.session.resource('ec2', region_name=region)
                image = self.ec2_or.Image(ami_id)
                image_name = image.name
                filter = [{'Name': 'name', 'Values': [image_name]}]
                imageCollection = self.ec2.images.filter(Filters=filter)
                image_id = ''
                for image in imageCollection:
                    image_id = image.id

                return image_id
            else:
                self.ec2.Image(ami_id)
                return ami_id
        except ClientError as error:
            raise Exception("AMI-ID not found in specified REGION. Provide correct AMI-ID or associated REGION")

    @staticmethod
    def calculate_iops(volume_size):
        """Calculate number of IOPs."""
        if int(volume_size) < 34:
            return 100
        else:
            return (int(volume_size) * 3)

    def create_instances(self, volume_size, volume_type, ami_id, region,
    	instance_type, key_name, max_count, min_count):
        """Create one or more EC2 instances."""
        iops = self.calculate_iops(volume_size)
        ami_id = self.find_ami_id(ami_id, region)
        instance = self.ec2.create_instances(
            BlockDeviceMappings=[{
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': int(volume_size),
                    'VolumeType': volume_type,
                }
            }],
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MaxCount=int(max_count),
            MinCount=int(min_count),
            UserData=open("D:\\Training\\Git\\Projects\\AWS-Projects-With-Python\\EC2\\script.txt").read()
        )
        inst = instance[0]
        inst.wait_until_running()
        inst.reload()
        print(inst.public_dns_name)
