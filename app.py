#!/usr/bin/env python3
import datetime
import os

import yaml
from aws_cdk import core as cdk

from stacks.ec2_stack import EC2Stack
from stacks.lambda_layer_stack import LambdaLayerStack
from stacks.lambda_stack import LambdaStack
from stacks.s3_bucket_stack import S3BucketStack
from stacks.scheduler_stack import SchedulerStack
from stacks.sns_stack import SNSStack
from stacks.vpc_stack import VPCStack
from utils.keypair import Keypair

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r', encoding='UTF-8') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

ami = config['aws_ec2_ami']
aws_environment = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
aws_tags_list = []
for k, v in config['aws_tags'].items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})
environment = config['environment']
inbounds = config['aws_ec2_inbounds']
is_versioned = config['aws_s3_versioned']
project = config['project']
subscribers = config['subscribers']
vpc_cidr = config['aws_vpc_cidr']

app = cdk.App()
s3_bucket_stack = S3BucketStack(
    app, '-'.join([project, environment, 's3']),
    bucket_name='-'.join([project, environment, 's3']), is_versioned=is_versioned, env=aws_environment
)
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']), env=aws_environment)
lambda_stack = LambdaStack(app, '-'.join([project, environment, 'lambda']), env=aws_environment)
scheduler_stack = SchedulerStack(app, '-'.join([project, environment, 'scheduler']), env=aws_environment)
vpc_stack = VPCStack(app, '-'.join([project, environment, 'vpc']), vpc_cidr, env=aws_environment)
date_now = datetime.datetime.now().strftime("%Y%m%d")
ec2_stack = EC2Stack(
    app, '-'.join([project, environment, 'ec2']),
    vpc=vpc_stack.vpc, ami=ami, inbounds=inbounds,
    keypair_name=Keypair.create_keypair(
        keypair_name='-'.join([project, environment, date_now, 'key']), aws_tags=aws_tags_list
    ),
    env=aws_environment
)
sns_stack = SNSStack(app, '-'.join([project, environment, 'sns']), subscribers, env=aws_environment)
scheduler_stack.add_dependency(lambda_stack)
scheduler_stack.add_dependency(sns_stack)
lambda_stack.add_dependency(lambda_layer_stack)
lambda_stack.add_dependency(s3_bucket_stack)
ec2_stack.add_dependency(s3_bucket_stack)
ec2_stack.add_dependency(vpc_stack)
for key, value in config['aws_tags'].items():
    cdk.Tags.of(app).add(key, value or " ")
cdk.Tags.of(s3_bucket_stack).add("application", "S3")
cdk.Tags.of(lambda_layer_stack).add("application", "LambdaLayer")
cdk.Tags.of(lambda_stack).add("application", "Lambda")
cdk.Tags.of(scheduler_stack).add("application", "Scheduler")
cdk.Tags.of(vpc_stack).add("application", "VPC")
cdk.Tags.of(ec2_stack).add("application", "EC2")
cdk.Tags.of(sns_stack).add("application", "SNS")
app.synth()
