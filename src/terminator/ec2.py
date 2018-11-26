# -*- coding: utf-8 -*-
"""

This module define interface for EC2 instances

"""

from builders import AWSResource


class Instance(AWSResource):
    """
    Representation of an EC2 instance being processed
    """

    def __init__(self, client, instance):
        super(self.__class__, self).__init__(client, instance)

    def get_id(self):
        return self._instance.instance_id

    def get_status(self):
        return self._instance.state['Name'].lower()

    def get_tags(self):
        return sorted(self._instance.tags, key=lambda x: x['Key'])

    def get_name(self):
        result = ""
        for t_key, t_value in [(t['Key'], t['Value']) for t in self.get_tags()]:
            if t_key == "Name":
                result = t_value
                break
            else:
                result = self._instance.instance_id
        return result

    def start(self):
        self._instance.start()
        return True

    def stop(self):
        self._instance.stop()
        return True

    def destroy(self):
        self._instance.terminate()
