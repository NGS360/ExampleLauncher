# ExampleLauncher

Example Launcher using PAML

## Workflows

Main workflows are in CWL/

## Launcher

Launcher is in launcher/

Example of running launcher:

When running the launcher manually/locally, specific the platform you are using:

```{sh}
launcher.py -s sample_sheet.txt --platform SevenBridges --project_name my_project
```

When the launcher is run on a platform as a CWL tool, then the command will look like:

```{sh}
launcher.py -s sample_sheet.txt
```

In this case the platform and project will be determined at run-time by the environment variables the platform sets in the docker container where the launcher is ran.
