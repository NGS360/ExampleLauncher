config = {
    'Arvados': {
        'reference_project': '<fill in reference project uuid>',
        'reference_data': {
            "hg38": "/Reference_Files/hg38"
        },
        'workflows': {
            'per-sample-workflow': '<fill in workflow uuid>',
        }
    },
    'SevenBridges': {
        'reference_project': 'launcher_reference_project',
        'reference_data': {
            "hg38": "/reference_files/hg38"
        },
        'workflows': {
            'per-sample-workflow': 'org/project/workflow',
        }
    }
}