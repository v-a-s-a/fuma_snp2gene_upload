# Upload files to FUMA

Some disclaimers: not guaranteed to work/be-stable. Storing any login information in plain text is a bad idea.

# Installation

Clone the repository down:

    git clone 
  
If using conda to manage your environments, create a new `conda` environment:

    conda create --name fuma_upload --file spec-file.txt
    source activate fuma_upload

Otherwise, you can install dependencies from the `spec-file.txt` file as you like.

# Usage

    usage: snp2gene_upload.py [-h] [--email EMAIL] [--password PASSWORD]
                              [--daner DANER_FILEPATH] [--job-name JOB_NAME]

    Submit a daner formatted file to FUMA: http://fuma.ctglab.nl/

    optional arguments:
      -h, --help            show this help message and exit
      --email EMAIL         The email address associated with your FUMA account.
      --password PASSWORD   Your FUMA account password.
      --daner DANER_FILEPATH
                            Location of the daner file you are trying to upload.
      --job-name JOB_NAME   The name of the job submitted to FUMA. Helpful for
                            finding your results later on.
