#!/usr/bin/python

# -*- coding: utf-8 -*-

import boto3

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
        tag_item=dict()
        for item in data.items():
            tag_item['Key'] = items[0]
            tag_item['Value'] = items[1]
            tags.append(tags)
        self.ec2.create_tags(
            Resource=[resource_id],
            Tags=tags
        )
