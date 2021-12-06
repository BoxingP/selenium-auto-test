import os
import shutil

import boto3


def download_files_from_s3(local_path, s3_bucket=os.environ['S3_BUCKET'], s3_directory=''):
    if not os.path.exists(local_path):
        print('Making download directory "%s" ...' % local_path)
        os.makedirs(local_path)
    client = boto3.client('s3')

    paginator = client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=s3_bucket, Prefix=s3_directory):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if key[-1] == '/':
                    continue
                absolute_path = os.path.join(local_path, *(key.split('/')[1:-1]))
                if not os.path.exists(absolute_path):
                    os.makedirs(absolute_path)
                client.download_file(Bucket=s3_bucket, Key=key,
                                     Filename=os.path.join(absolute_path, key.split('/')[-1]))


def get_report():
    local_path = '/var/allure_reports'
    report_path = 'allure_reports/'
    local_reports_path = os.path.join(local_path, report_path)

    if os.path.exists(local_reports_path):
        shutil.rmtree(local_reports_path)
    download_files_from_s3(local_path, s3_directory=report_path)


if __name__ == '__main__':
    get_report()
