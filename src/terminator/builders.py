# -*- coding: utf-8 -*-
"""

This module define interface to use for any AWS Resources which
should be managed by Terminator

"""

from __future__ import print_function
from abc import ABCMeta, abstractmethod


class AWSResource:
    """
    Define interface ro any type of resources
    """
    __metaclass__ = ABCMeta

    def __init__(self, client, instance):
        if client is None:
            raise ValueError("Missed client")
        if instance is None:
            raise ValueError("Missed instance")

        self._client = client
        self._instance = instance

    @abstractmethod
    def get_id(self):
        """ Amazon ID of the resource """
        raise NotImplementedError()

    @abstractmethod
    def get_status(self):
        """ The current status of the resource, either running or stopped """
        raise NotImplementedError()

    @abstractmethod
    def get_tags(self):
        """ List of tags of the resource sorted by tag name """
        raise NotImplementedError()

    @abstractmethod
    def get_name(self):
        """ Tag Name of the resource"""
        raise NotImplementedError()

    @abstractmethod
    def start(self):
        """ Start the resource """
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        """ Stop the resource """
        raise NotImplementedError()

    @abstractmethod
    def destroy(self):
        """ Destroy the resource """
