#!/usr/bin/env python3
import datetime
import os

import yaml
from aws_cdk import core as cdk

from auto_test_cdk.ec2_stack import EC2Stack
from auto_test_cdk.lambda_layer_stack import LambdaLayerStack
from auto_test_cdk.lambda_stack import LambdaStack
from auto_test_cdk.s3_bucket_stack import S3BucketStack
from auto_test_cdk.scheduler_stack import SchedulerStack
from auto_test_cdk.sns_stack import SNSStack
from auto_test_cdk.vpc_stack import VPCStack
from utils.keypair import Keypair

with open('aws_tags.yaml', 'r', encoding='UTF-8') as file:
    aws_tags = yaml.load(file, Loader=yaml.SafeLoader)
project = aws_tags['project'].lower().replace(' ', '-')
environment = aws_tags['environment']
aws_tags_list = []
for k, v in aws_tags.items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})
subscribers = [aws_tags['application owner']]

app = cdk.App()
s3_bucket_stack = S3BucketStack(app, '-'.join([project, environment, 's3']),
                                env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                    region=os.getenv("CDK_DEFAULT_REGION")))
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']),
                                      env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                          region=os.getenv("CDK_DEFAULT_REGION")))
lambda_stack = LambdaStack(app, '-'.join([project, environment, 'lambda']),
                           env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                               region=os.getenv("CDK_DEFAULT_REGION")))
scheduler_stack = SchedulerStack(app, '-'.join([project, environment, 'scheduler']),
                                 env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                     region=os.getenv("CDK_DEFAULT_REGION")))
vpc_stack = VPCStack(app, '-'.join([project, environment, 'vpc']),
                     env=cdk.Environment(
                         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
date_now = datetime.datetime.now().strftime("%Y%m%d")
ec2_stack = EC2Stack(app, '-'.join([project, environment, 'ec2']),
                     vpc_stack.vpc,
                     Keypair.create_keypair(
                         keypair_name='-'.join([project, environment, date_now, 'key']), aws_tags=aws_tags_list),
                     env=cdk.Environment(
                         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
sns_stack = SNSStack(app, '-'.join([project, environment, 'sns']), subscribers,
                     env=cdk.Environment(
                         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
scheduler_stack.add_dependency(lambda_stack)
scheduler_stack.add_dependency(sns_stack)
lambda_stack.add_dependency(lambda_layer_stack)
lambda_stack.add_dependency(s3_bucket_stack)
ec2_stack.add_dependency(s3_bucket_stack)
ec2_stack.add_dependency(vpc_stack)
for key, value in aws_tags.items():
    cdk.Tags.of(app).add(key, value or " ")
cdk.Tags.of(s3_bucket_stack).add("application", "S3")
cdk.Tags.of(lambda_layer_stack).add("application", "LambdaLayer")
cdk.Tags.of(lambda_stack).add("application", "Lambda")
cdk.Tags.of(scheduler_stack).add("application", "Scheduler")
cdk.Tags.of(vpc_stack).add("application", "VPC")
cdk.Tags.of(ec2_stack).add("application", "EC2")
cdk.Tags.of(sns_stack).add("application", "SNS")
app.synth()
