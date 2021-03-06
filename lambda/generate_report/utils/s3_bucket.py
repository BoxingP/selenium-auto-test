import os

import boto3
import botocore


class S3Bucket(object):
    def __init__(self, s3_bucket):
        self.client = boto3.client('s3')
        self.s3_bucket = s3_bucket

    def download_files_from_s3(self, local_path, s3_directory=''):
        if not os.path.exists(local_path):
            print('Making download directory "%s" ...' % local_path)
            os.makedirs(local_path)
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.s3_bucket, Prefix=s3_directory):
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    if key[-1] == '/':
                        continue
                    absolute_path = os.path.join(local_path, *(key.split('/')[0:-1]))
                    if not os.path.exists(absolute_path):
                        os.makedirs(absolute_path)
                    self.client.download_file(Bucket=self.s3_bucket, Key=key,
                                              Filename=os.path.join(absolute_path, key.split('/')[-1]))

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

    def empty_s3_directory(self, s3_directory):
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.s3_bucket, Prefix=s3_directory):
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    print('Deleting %s ...' % key)
                    self.client.delete_object(Bucket=self.s3_bucket, Key=key)
