import os
import shutil
import subprocess

import boto3


def download_files_from_s3(local_path, s3_bucket=os.environ['s3_bucket_name'], s3_directory=''):
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
                absolute_path = os.path.join(local_path, *(key.split('/')[0:-1]))
                if not os.path.exists(absolute_path):
                    os.makedirs(absolute_path)
                client.download_file(Bucket=s3_bucket, Key=key,
                                     Filename=os.path.join(absolute_path, key.split('/')[-1]))


def upload_files_to_s3(local_directory, s3_bucket=os.environ['s3_bucket_name'], s3_directory=''):
    client = boto3.client('s3')
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, local_directory)
            s3_path = os.path.join(s3_directory, relative_path)

            print('Uploading %s ...' % s3_path)
            client.upload_file(file_path, s3_bucket, s3_path)


def move_files_from_directory_to_another(source, target):
    if os.path.exists(source):
        files = os.listdir(source)
        if not os.path.exists(target):
            os.makedirs(target)
        for file in files:
            shutil.move(os.path.join(source, file), os.path.join(target, file))


def empty_s3_directory(s3_directory, s3_bucket=os.environ['s3_bucket_name']):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=s3_bucket, Prefix=s3_directory):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                print('Deleting %s ...' % key)
                client.delete_object(Bucket=s3_bucket, Key=key)


def lambda_handler(event, context):
    local_path = '/tmp'
    result_path = 'allure_results/'
    report_path = 'allure_reports/'
    local_results_path = os.path.join(local_path, result_path)
    local_reports_path = os.path.join(local_path, report_path)

    if os.path.exists(local_results_path):
        shutil.rmtree(local_results_path)
    download_files_from_s3(local_path, s3_directory=result_path)
    if not os.path.exists(local_results_path):
        return
    download_files_from_s3(local_path, s3_directory=report_path + 'history/')
    local_history_path = os.path.join(local_path, report_path, 'history/')
    move_files_from_directory_to_another(local_history_path, os.path.join(local_results_path, 'history/'))
    subprocess.run(['/opt/allure-2.16.1/bin/allure', 'generate', '-c', local_results_path, '-o', local_reports_path])
    upload_files_to_s3(local_reports_path, s3_directory=report_path)
    empty_s3_directory(result_path)


if __name__ == '__main__':
    lambda_handler(None, None)
