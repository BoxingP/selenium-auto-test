#!/usr/bin/env python3
import os

import yaml
from aws_cdk import core as cdk

from auto_test_cdk.lambda_layer_stack import LambdaLayerStack
from auto_test_cdk.lambda_stack import LambdaStack
from auto_test_cdk.s3_bucket_stack import S3BucketStack

with open('aws_tags.yaml', 'r', encoding='UTF-8') as file:
    aws_tags = yaml.load(file, Loader=yaml.SafeLoader)
project = aws_tags['project'].lower().replace(' ', '-')
environment = aws_tags['environment']
aws_tags_list = []
for k, v in aws_tags.items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})

app = cdk.App()
s3_bucket_stack = S3BucketStack(app, '-'.join([project, environment, 's3']),
                                env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                    region=os.getenv("CDK_DEFAULT_REGION")))
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']),
                                      env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                          region=os.getenv("CDK_DEFAULT_REGION")))
lambda_stack = LambdaStack(app, '-'.join([project, environment, 'lambda']),
                           lambda_layer_stack.layers, s3_bucket_stack.allure_results_bucket,
                           env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                               region=os.getenv("CDK_DEFAULT_REGION")))
for key, value in aws_tags.items():
    cdk.Tags.of(app).add(key, value or " ")
cdk.Tags.of(s3_bucket_stack).add("application", "S3")
cdk.Tags.of(lambda_layer_stack).add("application", "LambdaLayer")
cdk.Tags.of(lambda_stack).add("application", "Lambda")
app.synth()
