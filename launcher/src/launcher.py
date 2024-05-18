#!/usr/bin/env python3 
'''
Skeleton of a generic launcher that can be applied to most pipelines
'''
import argparse
import logging
import sys

from cwl_platform import SUPPORTED_PLATFORMS, PlatformFactory

import pipeline_config
from samplesheet import read_samplesheet

def copy_reference_data(platform, platform_config, reference_project, project):
    ''' Copy reference data from reference project to the working project '''
    reference_files = platform_config['reference_data']
    for ref_name, ref_path in reference_files.items():
        platform.copy_folder(reference_project, ref_path, project)

def copy_workflows(platform_config, platform, project):
    ''' Copy reference workflows to project '''
    workflows = {}
    for wf_name, wf_id in platform_config['workflows'].items():
        workflow = platform.copy_workflow(wf_id, project)
        workflows[wf_name] = workflow
    return workflows

def get_default_per_sample_workflow_parameters(platform, project):
    # In this example workflow, there are not default parameters to be
    # used across samples.
    return {}

def run_persample_workflow(samples, workflow, parameters, platform, project):
    parameters = get_default_per_sample_workflow_parameters(platform, project)

def do_work(args, platform, project):
    ''' Do the work of the launcher '''
    # Read the samplesheet
    samples = read_samplesheet(args.sample_sheet)

    # Copy reference workflow(s) to project
    workflows = copy_workflows(
        pipeline_config.config[args.platform], platform, project)

    # Copy reference data
    reference_project = platform.get_project_by_name(
        pipeline_config.config[args.platform]['reference_project'])

    copy_reference_data(platform, pipeline_config.config[args.platform], reference_project, project)

    # Run the per-sample workflow
    samples = run_persample_workflow(samples, workflows['workflow'], platform, project)
    samples = wait_for_tasks(samples, platform, project)
    '''
    # Run merge workflow
    merge_parameters = get_default_merge_parameters(args, platform, project)
    merge_workflow = run_merge_workflow(samples, merge_parameters, platform, project)
    merge_workflow = wait_for_tasks(merge_workflow, platform, project)

    # Stage files for output
    outputs = construct_output_files(merge_workflow, platform, project)
    platform.stage_output_files(outputs, platform, project)
    '''


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
