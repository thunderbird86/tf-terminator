# -*- coding: utf-8 -*-
"""

This module define interface to get information from AWS account

"""
from __future__ import print_function

import boto3
from ec2 import Instance


def get_all_regions():
    """
    Returns a list of available AWS regions
    """
    return [x['RegionName'] for x in boto3.client('ec2').describe_regions()['Regions']]


def get_instances_in_region(region):
    """
    Returns a list of all the type of instances, and their instances, managed
    by the scheduler
    :return:
    """
    ec2 = boto3.resource('ec2', region_name=region)

    return {
        'EC2': [Instance(ec2, resource) for resource in ec2.instances.all()],
    }
