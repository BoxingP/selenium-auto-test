import os
import shutil
import subprocess

from utils.database import Database
from utils.log import Log
from utils.s3_bucket import S3Bucket


def move_files_from_directory_to_another(source, target):
    if os.path.exists(source):
        files = os.listdir(source)
        if not os.path.exists(target):
            os.makedirs(target)
        for file in files:
            shutil.move(os.path.join(source, file), os.path.join(target, file))


def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_allure_reports(s3, local_path):
    result_path = 'allure_results'
    report_path = 'allure_reports'
    local_results_path = os.path.join(local_path, result_path)
    local_reports_path = os.path.join(local_path, report_path)

    if os.path.exists(local_results_path):
        shutil.rmtree(local_results_path)
    s3.download_files_from_s3(local_path=local_path, s3_directory=os.path.join(result_path, '').replace('\\', '/'))
    if not os.path.exists(local_results_path):
        return
    s3.download_files_from_s3(
        local_path=local_path,
        s3_directory=os.path.join(report_path, 'history', '').replace('\\', '/')
    )
    local_history_path = os.path.join(local_path, report_path, 'history')
    move_files_from_directory_to_another(local_history_path, os.path.join(local_results_path, 'history'))
    subprocess.run(['/opt/allure-2.16.1/bin/allure', 'generate', '-c', local_results_path, '-o', local_reports_path])
    s3.upload_files_to_s3(local_directory=local_reports_path, s3_directory=report_path)
    s3.empty_s3_directory(s3_directory=os.path.join(result_path, '').replace('\\', '/'))


def save_log_to_db(s3, local_path):
    logs_path = 'logs'
    local_logs_path = os.path.join(local_path, logs_path)
    local_log_file = os.path.join(local_logs_path, 'steps.log')
    s3.download_files_from_s3(local_path=local_path, s3_directory=os.path.join(logs_path, '').replace('\\', '/'))
    log_database = Database()
    with open(local_log_file) as file:
        lines = file.readlines()
    if lines:
        for line in lines:
            log = Log(line)
            log_database.insert_log(log)
    s3.empty_s3_directory(s3_directory=os.path.join(logs_path, '').replace('\\', '/'))


def lambda_handler(event, context):
    local_path = os.path.join(os.path.abspath(os.sep), 'tmp')
    s3 = S3Bucket(s3_bucket=os.environ['s3_bucket_name'])
    generate_allure_reports(s3, local_path)
    save_log_to_db(s3, local_path)
    empty_directory(local_path)


if __name__ == '__main__':
    lambda_handler(None, None)
