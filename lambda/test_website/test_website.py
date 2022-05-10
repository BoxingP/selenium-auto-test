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
                extra_args = None
                if file_path.endswith('.png'):
                    extra_args = {'ContentType': 'image/png'}
                client.upload_file(file_path, s3_bucket, s3_path, ExtraArgs=extra_args)


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


def add_date_tag(logs_dir):
    filenames = []
    current = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    for root, dirs, files in os.walk(logs_dir):
        filenames.extend(files)
        break
    if filenames:
        for filename in filenames:
            new_filename = '{0}_{2}.{1}'.format(*filename.rsplit('.', 1) + [current])
            os.rename(os.path.join(logs_dir, filename), os.path.join(logs_dir, new_filename))


def lambda_handler(event, context):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    tmp_dir = os.path.join(os.path.abspath(os.sep), 'tmp')
    allure_results_dir = os.path.join(tmp_dir, config['allure_results_dir'])
    screenshots_dir = os.path.join(tmp_dir, config['screenshots_dir'])
    json_report_file = os.path.join(tmp_dir, 'report.json')
    logs_dir = os.path.join(tmp_dir, config['logs_dir'])
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    pytest.main(
        [tests_dir, f"--alluredir={allure_results_dir}", '--cache-clear', f"--json={json_report_file}", '-n', '5']
    )
    generate_env_properties(allure_results_dir, config)
    upload_files_to_s3(allure_results_dir, s3_directory=config['allure_results_dir'])
    upload_files_to_s3(screenshots_dir, s3_directory=config['screenshots_dir'])
    add_date_tag(logs_dir)
    upload_files_to_s3(logs_dir, s3_directory=config['logs_dir'])
    with open(json_report_file, 'r', encoding='utf-8') as file:
        report = json.loads(file.read())
    empty_directory(directory=tmp_dir)

    return report


if __name__ == '__main__':
    lambda_handler(None, None)
