#!/usr/bin/env python
'''
Hack-y program to submit daner files to FUMA.
'''

import requests as req
import lxml.html
from requests_toolbelt import MultipartEncoder
import os
import argparse as arg


def __submit_fuma_job(email, password, daner_filepath, job_name):
    with req.session() as sesh:
        # GET login to FUMA + CSRF token
        login = sesh.get('http://fuma.ctglab.nl/login')
        login.raise_for_status()
        login_html = lxml.html.fromstring(login.text)
        hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
        login_token = {x.attrib['name']: x.attrib['value'] for x in hidden_inputs if x.attrib['name']=='_token'}

        fuma_home = sesh.post('http://fuma.ctglab.nl/login',
            data={'email': email,
                  'password': password,
                  '_token': login_token['_token']})
        fuma_home.raise_for_status()

        # GET snp2gene form + CSRF token
        snp2gene = sesh.get('http://fuma.ctglab.nl/snp2gene')
        snp2gene.raise_for_status()
        snp2gene_html = lxml.html.fromstring(snp2gene.text)
        snp2gene_hidden_inputs = snp2gene_html.xpath(r'//form//input[@type="hidden"]')
        snp2gene_token = {x.attrib['name']: x.attrib['value'] for x in snp2gene_hidden_inputs if x.attrib['name']=='_token'}

        # POST a new FUMA job
        multipart_encoder = MultipartEncoder({
            '_token': snp2gene_token['_token'],
            'GWASsummary': (os.path.basename(daner_filepath), open(daner_filepath, 'rb'), 'application/x-gzip'),
            'chrcol': '',
            'poscol': '',
            'rsIDcol': '',
            'pcol': '',
            'eacol': '',
            'neacol': '',
            'orcol': '',
            'becol': '',
            'secol': '',
            'leadSNPs': ('', '', 'application/octet-stream'),
            'regions': ('', 'application/octet-stream'),
            'N': '77096',
            'leadP': '5e-8',
            'r2': '0.6',
            'gwasP': '0.05',
            'refpanel': '1KG/Phase3/EUR',
            'KGSNPs': 'Yes',
            'maf': '0.01',
            'mergeDist': '250',
            'posMap': 'on',
            'posMapWindow': '10',
            'posMapCADDth': '12.37',
            'posMapRDBth': '7',
            'posMapChr15Max': '7',
            'posMapChr15Meth': 'any',
            'sigeqtlCheck': 'on',
            'eqtlP': '1e-3',
            'eqtlMapCADDth': '12.37',
            'eqtlMapRDBth': '7',
            'eqtlMapChr15Max': '7',
            'eqtlMapChr15Meth': 'any',
            'ciFileN': '0',
            'ciMapFDR': '1e-6',
            'ciMapPromWindow': '250-500',
            'ciMapCADDth': '12.37',
            'ciMapRDBth': '7',
            'ciMapChr15Max': '7',
            'ciMapChr15Meth': 'any',
            'genetype[]': 'protein_coding',
            'MHCregion': 'exMHC',
            'MHCopt': 'annot',
            'extMHCregion': '',
            'NewJobTitle': job_name,
            'SubmitNewJob': 'Submit Job',
            })
        job_submit = sesh.post('http://fuma.ctglab.nl/snp2gene/newJob',
            data=multipart_encoder,
            headers={'Content-Type': multipart_encoder.content_type})
        job_submit.raise_for_status()

        print('Status: SUBMITTED SUCCESSFULLY\n'
              'Jobname: \'{jobname}\'\n'
              'Daner file: {daner}\n'
              '\n'
              'Check http://fuma.ctglab.nl/snp2gene#joblist-panel for the status of your job.'.format(
                  jobname=job_name, daner=daner_filepath))


if __name__ == '__main__':
    parser = arg.ArgumentParser(description='Submit a daner formatted file to FUMA: \n\thttp://fuma.ctglab.nl/')
    parser.add_argument('--email', dest='email',
                        help='The email address associated with your FUMA account.')
    parser.add_argument('--password', dest='password',
                        help='Your FUMA account password.')
    parser.add_argument('--daner', dest='daner_filepath',
                        help='Location of the daner file you are trying to upload.')
    parser.add_argument('--job-name', dest='job_name',
                        help='The name of the job submitted to FUMA. Helpful for finding your results later on.')
    args = parser.parse_args()

    # check arguments
    if not os.path.exists(args.daner_filepath):
        raise ValueError('File {} cannot be located.'.format(args.daner_filepath))
    
    if not args.daner_filepath.endswith('.gz'):
        raise ValueError('Please make sure your file is gzipped with file extention \'.gz\'.')

    # submit job to FUMA
    __submit_fuma_job(email=args.email,
                      password=args.password,
                      daner_filepath=args.daner_filepath,
                      job_name=args.job_name)
