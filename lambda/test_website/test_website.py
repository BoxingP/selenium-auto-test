import json
import os
import shutil
import sys
from io import StringIO

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


def generate_env_properties(target_path, config_path=os.path.join(os.path.dirname(__file__), 'config.json')):
    with open(config_path, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    with open(os.path.join(target_path, 'environment.properties'), 'w', encoding='UTF-8') as file:
        line1 = 'Browser=%s\n' % config['browser']
        line2 = 'BrowserVersion=%s\n' % config['headless_chromium']
        line3 = 'Environment=%s\n' % config['environment']
        line4 = 'Python=%s\n' % config['python']
        line5 = 'TestedPage=%s' % config['tested_page']
        file.writelines([line1, line2, line3, line4, line5])


def empty_directory(directory='/tmp'):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def lambda_handler(event, context):
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    allure_results_dir = '/tmp/allure_results'

    original_output = sys.stdout
    sys.stdout = StringIO()
    pytest.main([tests_dir, '--alluredir=' + allure_results_dir, '--cache-clear', '-p', 'no:terminal'])
    output = sys.stdout.getvalue()
    number_of_failed = int(output.upper())
    sys.stdout.close()
    sys.stdout = original_output
    generate_env_properties(allure_results_dir)
    upload_files_to_s3(allure_results_dir, s3_directory='allure_results')
    empty_directory()

    return number_of_failed


if __name__ == '__main__':
    lambda_handler(None, None)
