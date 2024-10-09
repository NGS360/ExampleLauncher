cwlVersion: v1.2
class: CommandLineTool
label: Example Launcher

requirements:
  WorkReuse:
    enableReuse: false
  DockerRequirement:
    dockerPull: ngsbioinformatics/examplelauncher:latest

baseCommand: ["/opt/launcher/launcher.py"]

inputs:
  sample_sheet:
    type: File
    inputBinding:
      prefix: -s

outputs:
  log:
    type: File
    outputBinding:
      glob: '*.log'
