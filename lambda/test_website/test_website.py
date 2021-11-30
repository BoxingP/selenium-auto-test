import os

import boto3
import botocore
import pytest


def upload_files_to_s3(local_directory, s3_bucket=os.environ['s3_bucket_name'], s3_directory=''):
    client = boto3.client('s3')
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, local_directory)
            s3_path = os.path.join(s3_directory, relative_path)

            print('Searching "%s" in "%s"' % (s3_path, s3_bucket))
            try:
                client.head_object(Bucket=s3_bucket, Key=s3_path)
                print('File found, skipped %s' % s3_path)
            except botocore.exceptions.ClientError:
                print('Uploading %s ...' % s3_path)
                client.upload_file(file_path, s3_bucket, s3_path)


def lambda_handler(event, context):
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    allure_results_dir = '/tmp/allure_results'

    pytest.main([tests_dir, '--alluredir=' + allure_results_dir, '--cache-clear'])

    upload_files_to_s3(allure_results_dir, s3_directory='allure_results')


if __name__ == '__main__':
    lambda_handler(None, None)
