cwlVersion: v1.2
class: Workflow

inputs:
  sample_name:
    type: string
  fastq1:
    type: File
  fastq2:
    type: File

steps:
  fastqc1:
    in:
      reads_file: fastq1
    run:
      tools/fastqc.cwl
    out: [zipped_file, html_file, summary_file]

  fastqc2:
    in:
      reads_file: fastq2
    run:
      tools/fastqc.cwl
    out: [zipped_file, html_file, summary_file]

outputs:
  fastqc_report1:
    type: File
    outputSource: fastqc1/html_file

  fastqc_report2:
    type: File
    outputSource: fastqc2/html_file

