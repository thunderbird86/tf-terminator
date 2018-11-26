# -*- coding: utf-8 -*-
"""

This module contain main class for management AWS resources

"""

from __future__ import print_function

import datetime
import re
import json

from urllib import request
from aws import AWS
from main import protection_tag
# Prefix of all tags that are schedulers


class Terminator:
    """
    Main class for this lambda

    """

    current_date = datetime.datetime.now()

    destroy_list = []
    scheduler_list = []
    white_list = []

    def __init__(self, run_on_regions, dry_run):
        """
        Run terminator for specified regions
        """

        print("Running Terminator")
        print("Protection tag is {0}".format(protection_tag))

        # Going through provided AWS regions
        try:
            if run_on_regions == []:
                run_on_regions = AWS.get_all_regions()

            for region in run_on_regions:
                print("\nWorking on region \"{0}\":".format(region))

                for i_type, i_list in AWS.get_instances_in_region(region).items():
                    print(" Checking {0} resources:".format(i_type))

                    for instance in i_list:
                        if instance.get_status() == "terminated":
                            continue
                        else:
                            if dry_run is True:
                                print("     Dry run detected")
                                self.build_victims_list(instance)
                            else:
                                print("     Perform actions")
                                self.perform_action(instance)

                    self.send_notification(dry_run, region)


        except Exception as e:
            print(e)

    def process_instance(self, instance):
        """
        Process the tags of a single instance and decides what to do with it
        """
        print("     Instance \"{0}\" state is \"{1}\"".format(instance.get_id(), instance.get_status()))

        date_template = re.compile(r"^\s*(3[01]|[12][0-9]|0?[1-9])\-(1[012]|0?[1-9])\-((?:19|20)\d{2})\s*$")
        bool_template = re.compile("^[T-t][R-r][U-u][E-e]")
        result = ""

        for t_key, t_value in [(t['Key'], t['Value']) for t in instance.get_tags()]:
            # Extract the information in the Key
            # print("     Compare is {0} - {1}".format(t_key, t_value))

            if t_key == protection_tag:
                if bool_template.match(t_value):
                    print("     Will be destroyed")
                    result = "skip"

                elif date_template.match(t_value):

                    protection_date = datetime.datetime.strptime(t_value, "%d-%m-%Y")

                    if self.current_date > protection_date:
                        print("     Date missed, destroy {0}".format(instance.get_id()))
                        result = "destroy"

                    else:
                        print("     Do not destroy instance {0}, until {1}".format(instance.get_id(), t_value))
                        result = "schedule"
                else:
                    result = "destroy"
            else:
                result = "destroy"

        return result

    def build_victims_list(self, instance):
        """
        Execute define actions to provided resources
        :param instance:
        :return:
        """

        i = self.process_instance(instance)

        if i == "skip":
            self.white_list.append(instance.get_name())
        elif i == "schedule":
            self.scheduler_list.append(instance.get_name())
        elif i == "destroy":
            self.destroy_list.append(instance.get_name())

    def send_notification(self, dry_run, region):
        """
        Send notification to slack
        :param region:
        :return:
        """

        if dry_run:
            text = '!!TEST!! \
                    \n`For region {0}` \
                    \n`Connor family` {1}, \
                    \n`I\'ll be back` {2}, \
                    \n`You can run, but you can\'t hide ` {3}'.format(region, self.white_list, self.scheduler_list, self.destroy_list)
        else:
            text = "`I'll be back`"

        print(text)
        exit(0)

        post = {"text": "{0}".format(text)}

        try:
            json_data = json.dumps(post)
            req = request.Request("https://hooks.slack.com/services/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",
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'})
            request.urlopen(req)
        except Exception as e:
            print(e)

    def perform_action(self, instance):

        i = self.process_instance(instance)

        if i == "skip":
            pass
        elif i == "schedule":
            instance.stop()
        elif i == "destroy":
            instance.destroy()