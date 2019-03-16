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


if __name__ == '__main__':
		cli()
