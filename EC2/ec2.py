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
