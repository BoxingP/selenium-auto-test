import os

import boto3
import botocore


class S3Bucket(object):
    def __init__(self, s3_bucket):
        self.client = boto3.client('s3')
        self.s3_bucket = s3_bucket

    def upload_files_to_s3(self, local_directory, s3_directory='', is_replace=False):
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path).replace('\\', '/')

                if is_replace:
                    self.upload_file_to_s3(file_path, s3_path)
                else:
                    try:
                        print(f'Searching "{s3_path}" in "{self.s3_bucket}"')
                        self.client.head_object(Bucket=self.s3_bucket, Key=s3_path)
                        print(f"File found, skipped {s3_path}")
                    except botocore.exceptions.ClientError:
                        self.upload_file_to_s3(file_path, s3_path)

    def upload_file_to_s3(self, file_path, s3_path):
        extra_args = None
        if file_path.endswith('.png'):
            extra_args = {'ContentType': 'image/png'}
        print(f"Uploading {s3_path} ...")
        self.client.upload_file(file_path, self.s3_bucket, s3_path, ExtraArgs=extra_args)
