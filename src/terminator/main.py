import os

from terminator import *

dry_run = os.environ.get('DRY_RUN')
protection_tag = "Terminator_omit"


def lambda_handler(event, context):
    """ AWS Lambda entry point """
    aws_regions = AWS.run_on_regions = filter(None, os.environ.get('RUN_ON_REGIONS', "").split(','))
    Terminator(aws_regions, dry_run)


if __name__ == '__main__':
    """ Console entry point """
    print("Execution from Command Line\n")

    aws_regions = AWS.run_on_regions = filter(None, os.environ.get('RUN_ON_REGIONS', "").split(','))
    Terminator(aws_regions, dry_run)
