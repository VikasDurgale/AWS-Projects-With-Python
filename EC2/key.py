#!/usr/bin/python

# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError


class KeyManager:
    """Manage KeyPairs."""

    def __init__(self, session):
        """Create a KeyManager object."""
        self.session = session
        self.ec2 = self.session.resource('ec2')

    def list_keys(self):
        """List all the available Keys."""
        for key in self.ec2.key_pairs.all():
            print(key.key_name)

    def delete_key(self, key_name):
        """Deletes specified key."""
        key = self.ec2.KeyPair(key_name)
        response = key.delete()
        if response:
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("Deleted Key.")
            else:
                print("Key not Deleted.")

    def create_key(self, key_name):
        """Create new KeyPair for EC2 instance"""
        key_pair = self.ec2.create_key_pair(KeyName=key_name)
        key_path = key_name + '.pem'
        with open(key_path, 'w') as key_file:
            key_file.write(key_pair.key_material)
            print("Key Created.")

    def check_key(self, key_name):
        """Check whether the ket exists or not."""
        try:
            key = self.ec2.key_pairs.filter(
                    KeyNames=[key_name]
                )
            for k in key:
                return True
        except ClientError as error:
            return False
