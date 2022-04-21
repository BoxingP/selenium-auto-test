import datetime
import json
import os
import shutil

import boto3
import botocore
import pytest


def upload_files_to_s3(local_directory, s3_bucket=os.environ['s3_bucket_name'], s3_directory=''):
    client = boto3.client('s3')
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, local_directory)
            s3_path = os.path.join(s3_directory, relative_path).replace('\\', '/')

            print(f'Searching "{s3_path}" in "{s3_bucket}"')
            try:
                client.head_object(Bucket=s3_bucket, Key=s3_path)
                print(f"File found, skipped {s3_path}")
            except botocore.exceptions.ClientError:
                print(f"Uploading {s3_path} ...")
                client.upload_file(file_path, s3_bucket, s3_path)


def generate_env_properties(target_path, config):
    with open(os.path.join(target_path, 'environment.properties'), 'w', encoding='UTF-8') as file:
        line1 = f"Browser={config['browser']}\n"
        line2 = f"BrowserVersion={config['headless_chromium']}\n"
        line3 = f"Environment={config['environment']}\n"
        line4 = f"Python={config['python']}\n"
        line5 = f"MonitoredSite={config['base_url']}"
        file.writelines([line1, line2, line3, line4, line5])


def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def delete_files_in_s3(key_word: str, s3_bucket=os.environ['s3_bucket_name'], s3_directory=''):
    client = boto3.client('s3')
    objects = []
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=s3_bucket, Prefix=s3_directory)
    for obj in page_iterator.search(f'Contents[?contains(Key, `{key_word}`)][]'):
        if obj is None:
            break
        if not obj['Key'].endswith('/'):
            objects.append(obj['Key'])
    if objects:
        for obj in objects:
            print(f'Deleting {obj} ...')
            client.delete_object(Bucket=s3_bucket, Key=obj)


def update_start_flag(flag: str, local_directory: str, s3_directory=''):
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    flag_path = os.path.join(local_directory, f'{flag}_{datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")}.txt')
    with open(flag_path, 'w') as file:
        pass
    delete_files_in_s3(key_word=flag, s3_directory=s3_directory)
    upload_files_to_s3(local_directory, s3_directory=s3_directory)


def lambda_handler(event, context):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    tmp_dir = os.path.join(os.path.abspath(os.sep), 'tmp')
    allure_results_dir = os.path.join(tmp_dir, config['allure_results_dir'])
    screenshots_dir = os.path.join(tmp_dir, config['screenshots_dir'])
    json_report_file = os.path.join(tmp_dir, 'report.json')

    update_start_flag(flag='last_run_utc', local_directory=screenshots_dir, s3_directory=config['screenshots_dir'])
    pytest.main(
        [tests_dir, f"--alluredir={allure_results_dir}", '--cache-clear', f"--json={json_report_file}", '-n', '5']
    )
    generate_env_properties(allure_results_dir, config)
    upload_files_to_s3(allure_results_dir, s3_directory=config['allure_results_dir'])
    upload_files_to_s3(screenshots_dir, s3_directory=config['screenshots_dir'])
    with open(json_report_file, 'r', encoding='utf-8') as file:
        report = json.loads(file.read())
    empty_directory(directory=tmp_dir)

    return report


if __name__ == '__main__':
    lambda_handler(None, None)
