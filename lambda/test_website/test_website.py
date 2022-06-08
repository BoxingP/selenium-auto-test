import json
import os
import shutil

import pytest

from utils.s3_bucket import S3Bucket


def generate_env_properties(target_path, config):
    with open(os.path.join(target_path, 'environment.properties'), 'w', encoding='UTF-8') as file:
        line1 = f"Browser={config['browser']}\n"
        line2 = f"BrowserVersion={config['browser_version']}\n"
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


def lambda_handler(event, context):
    s3 = S3Bucket(s3_bucket=os.environ['s3_bucket_name'])
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
    s3.upload_files_to_s3(local_directory=allure_results_dir, s3_directory=config['allure_results_dir'])
    s3.upload_files_to_s3(local_directory=screenshots_dir, s3_directory=config['screenshots_dir'])
    s3.upload_files_to_s3(local_directory=logs_dir, s3_directory=config['logs_dir'], is_replace=True)
    with open(json_report_file, 'r', encoding='utf-8') as file:
        report = json.loads(file.read())
    empty_directory(directory=tmp_dir)

    return report


if __name__ == '__main__':
    lambda_handler(None, None)
