# -*- coding: utf-8 -*-
"""
This module contain main class for management AWS resources
"""

import datetime
import re
import json
import os

from urllib import request
from aws import *

protection_tag = "Terminator_omit"

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
        print("Dry run is {0}".format(dry_run))

        # Going through provided AWS regions
        try:
            if run_on_regions == []:
                run_on_regions = get_all_regions()
        except Exception as e:
            print(e)

        for region in run_on_regions:
            print("\nWorking on region \"{0}\":".format(region))

            for i_type, i_list in get_instances_in_region(region).items():
                print(" Checking {0} resources:".format(i_type))

                for instance in i_list:
                    if instance.get_status() == "terminated":
                        continue
                    else:
                        if dry_run.lower() == "true":
                            try:
                                self.build_victims_list(instance)
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                self.perform_action(instance)
                            except Exception as e:
                                print(e)

                self.send_notification(dry_run, region)

    def process_instance(self, instance):
        """
        Process the tags of a single instance and decides what to do with it
        """
        print("     Instance \"{0}\" state is \"{1}\"".format(instance.get_id(), instance.get_status()))

        date_template = re.compile(r"^\s*(3[01]|[12][0-9]|0?[1-9])\-(1[012]|0?[1-9])\-((?:19|20)\d{2})\s*$")

        for t_key, t_value in [(t['Key'], t['Value']) for t in instance.get_tags()]:

            if t_key == protection_tag:

                if t_value.lower() == 'true':
                    print("     Will be destroyed")
                    return "skip"

                elif date_template.match(t_value):

                    protection_date = datetime.datetime.strptime(t_value, "%d-%m-%Y")

                    if self.current_date > protection_date:
                        print("     Date missed, destroy {0}".format(instance.get_id()))
                        return "destroy"

                    else:
                        print("     Do not destroy instance {0}, until {1}".format(instance.get_id(), t_value))
                        return "schedule"
                else:
                    return "destroy"

        return "destroy"

    def build_victims_list(self, instance):
        """
        Execute define actions to provided resources
        :param instance:
        :return:
        """

        action = self.process_instance(instance)

        if action == "skip":
            self.white_list.append(instance.get_name())
        elif action == "schedule":
            self.scheduler_list.append(instance.get_name())
        elif action == "destroy":
            self.destroy_list.append(instance.get_name())

    def send_notification(self, dry_run, region):
        """
        Send notification to slack
        :param dry_run:
        :param region:
        :return:
        """

        msg = ""
        if dry_run.lower == "true":
            msg += "`For region {0}`".format(region)
            msg += "\n`Connor family:`"
            for resource in self.white_list:
                msg += "\n - {}".format(resource)
            msg += "\n`I\'ll be back:`"
            for resource in self.scheduler_list:
                msg += "\n - {}".format(resource)
            msg += "\n`You can run, but you can\'t hide:`"
            for resource in self.destroy_list:
                msg += "\n - {}".format(resource)
        else:
            msg += "`I'll be back`"

        post = {"text": "{0}".format(msg)}

        try:
            json_data = json.dumps(post)
            req = request.Request("https://hooks.slack.com/services/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",
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'})
            request.urlopen(req)
        except Exception as e:
            print(e)

    def perform_action(self, instance):

        action = self.process_instance(instance)

        print("Perform action - {}:".format(action))

        if action == "skip":
            pass
        elif action == "schedule":
            instance.stop()
        elif action == "destroy":
            instance.destroy()


def lambda_handler(event, context):
    """ AWS Lambda entry point """
    run_on_regions = event['run_on_regions']
    dry_run = event['dry_run']
    Terminator(run_on_regions, dry_run)


if __name__ == '__main__':
    """ Console entry point """
    print("Execution from Command Line\n")

    run_on_regions = filter(None, os.environ.get('RUN_ON_REGIONS', "").split(','))
    dry_run = os.environ.get('DRY_RUN')
    Terminator(run_on_regions, dry_run)
