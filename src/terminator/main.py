import os

from terminator import *

dry_run = bool(os.environ.get('DRY_RUN'))
protection_tag = "Terminator_omit"


def lambda_handler(event, context):
    """ AWS Lambda entry point """
    run_on_regions = filter(None, os.environ.get('RUN_ON_REGIONS', "").split(','))
    Terminator(run_on_regions, dry_run)


if __name__ == '__main__':
    """ Console entry point """
    print("Execution from Command Line\n")

    run_on_regions = filter(None, os.environ.get('RUN_ON_REGIONS', "").split(','))
    Terminator(run_on_regions, dry_run)
