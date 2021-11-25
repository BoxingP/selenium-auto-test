#!/usr/bin/env python3
import os

import yaml
from aws_cdk import core as cdk

from selenium_auto_test.lambda_layer_stack import LambdaLayerStack
from selenium_auto_test.lambda_stack import LambdaStack

with open('aws_tags.yaml', 'r', encoding='UTF-8') as file:
    aws_tags = yaml.load(file, Loader=yaml.SafeLoader)
project = aws_tags['project'].lower().replace(' ', '-')
environment = aws_tags['environment']
aws_tags_list = []
for k, v in aws_tags.items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})

app = cdk.App()
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']),
                                      env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                          region=os.getenv("CDK_DEFAULT_REGION")))
lambda_stack = LambdaStack(app, '-'.join([project, environment, 'lambda']),
                           lambda_layer_stack.pytest_layer,
                           lambda_layer_stack.pyyaml_layer,
                           lambda_layer_stack.selenium_layer,
                           lambda_layer_stack.chromedriver_layer,
                           env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                               region=os.getenv("CDK_DEFAULT_REGION")))
for key, value in aws_tags.items():
    cdk.Tags.of(app).add(key, value or " ")
cdk.Tags.of(lambda_layer_stack).add("application", "LambdaLayer")
cdk.Tags.of(lambda_stack).add("application", "Lambda")
app.synth()
