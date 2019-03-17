#!/usr/bin/python

# -*- coding: utf-8 -*-

import boto3
import click
from key import KeyManager
from ec2 import EC2Manager

session=None
key_manager = None
ec2_manager = None


@click.group()
@click.option('--profile', default=None,
	help="Use a given AWS profile")
def cli(profile):
	"""Python project to configure ec2 instances"""
	global session, key_manager, ec2_manager
	#session = boto3.session.Session(profile_name=profile)
	session_cfg = {}
	if profile:
		session_cfg['profile_name'] = profile
	session = boto3.session.Session(**session_cfg)
	key_manager = KeyManager(session)
	ec2_manager = EC2Manager(session)


@cli.command('list-instances')
def list_instances():
	"""List all the EC2 instances created"""
	ec2_manager.list_instances()


@cli.command('list-keys')
def list_keys():
	"""List all the available Keys."""
	key_manager.list_keys()


@cli.command('delete-key')
@click.argument('key_name')
def delete_key(key_name):
	"""Deletes specified key."""
	key_manager.delete_key(key_name)


@cli.command('create-key')
@click.argument('key_name')
def create_key(key_name):
	"""Create new KeyPair for EC2 instance"""
	key_manager.create_key(key_name)


@cli.command('create-tag', context_settings=dict(
	ignore_unknown_options=True,
	allow_extra_args=True
))
@click.argument('resource_id')
@click.pass_context
def create_tag(ctx, resource_id):
	"""Create's Tag for your EC2 instance."""
	data = dict()
	for item in ctx.args:
		data.update([item.split('=')])
	ec2_manager.create_tag(resource_id, data)


@cli.command('find-ami-id')
@click.argument('ami_id')
@click.argument('region')
def find_ami_id(ami_id, region):
	"""Find AMI ID from different region AMI ID."""
	ec2_manager.find_ami_id(ami_id, region)


@cli.command('create-instances')
@click.option('--volume-size', default='8',
	help='The size of the volume, in GiB.')
@click.option('--volume-type', default='gp2',
	help='The volume type: gp2, io1, st1, sc1, or standard.')
@click.option('--ami-id', default=None,
	help='The ID of the AMI.')
@click.option('--region', default=None,
	help='Region of ami_id provided.')
@click.option('--instance-type', default='t2.micro',
	help='The instance type.')
@click.option('--key-name', default=None,
	help='The name of the key pair.')
@click.option('--max-count', default='1',
	help='The maximum number of instances to launch.')
@click.option('--min-count', default='1',
	help='The minimum number of instances to launch.')
def create_instances(volume_size, volume_type, ami_id, region, instance_type,
	key_name, max_count, min_count):
	"""Create one or more EC2 instances."""
	if ami_id == None or key_name == None:
		raise Exception('ami-id not mentioned. check create-instances --help')
	if key_name == None:
		raise Exception('key-name not mentioned. check create-instances --help')
	if region == None:
		region = session.region_name
	key = key_manager.check_key(key_name)
	if key == False:
		raise Exception("Key not found")
	ec2_manager.create_instances(volume_size, volume_type, ami_id, region,
		instance_type, key_name, max_count, min_count)


if __name__ == '__main__':
		cli()
