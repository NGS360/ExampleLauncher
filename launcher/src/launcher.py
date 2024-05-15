#!/usr/bin/env python3 
'''
Skeleton of a generic launcher that can be applied to most pipelines
'''
import argparse
import logging
import sys

from cwl_platform import SUPPORTED_PLATFORMS, PlatformFactory

def do_work(args, platform, project):
    ''' Do the work of the launcher '''
    logging.info("Doing work...")

def main(argv):
    ''' Main Entry Point '''

    # Parse arguments
    args = parse_arguments(argv)

    # Start Logging
    logging.basicConfig(level=args.log_level)
    logging.info(args)

    # Construct and connect to platform
    if not args.platform:
        # See if we can figure out what platform we are running on.
        logging.info("No platform provided...detecting platform.")
        args.platform = PlatformFactory().detect_platform()
        logging.info("Detected platform: %s", args.platform)
    platform = PlatformFactory().get_platform(args.platform)
    platform.connect()

    # Get the project uuid either by its provided name or from this launcher's project
    if args.project_id:
        project = platform.get_project_by_id(args.project_id)
    elif args.project_name:
        project = platform.get_project_by_name(args.project_name)
    else:
        project = platform.get_project()

    if not project:
        logging.error("Could not determine project to run in")
        sys.exit(1)

    do_work(args, platform, project)

    logging.info("Done.")

def parse_arguments(argv):
    ''' Parse command line arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    parser.add_argument('-p', '--platform', default=None, choices=SUPPORTED_PLATFORMS.keys())

    # Allow user to provide platform project project to run in when running launcher locally.
    # These are not needed when the launcher is run on a platform.
    project = parser.add_mutually_exclusive_group(required=False)
    project.add_argument('--project_name', help="Project name where this workflow is executed")
    project.add_argument('--project_id', help="Project id/uuid where thi workflow is executed")

    parser.add_argument('-s', '--sample_sheet', required=True, help="Samplesheet for workflow")
    return parser.parse_args(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
