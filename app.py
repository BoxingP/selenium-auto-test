#!/usr/bin/env python3
import datetime
import os

import yaml
from aws_cdk import core as cdk

from stacks.lambda_layer_stack import LambdaLayerStack
from stacks.lambda_stack import LambdaStack
from stacks.load_balancer_stack import LoadBalancerStack
from stacks.s3_bucket_stack import S3BucketStack
from stacks.sns_stack import SNSStack
from stacks.step_functions_stack import StepFunctionsStack
from stacks.vpc_stack import VPCStack
from utils.config import get_config_value
from utils.keypair import Keypair

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r', encoding='UTF-8') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

aws_environment = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
aws_tags_list = []
aws_tags = get_config_value('aws.tags', config)
for k, v in aws_tags.items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})
project = get_config_value('project.name', config)
environment = get_config_value('project.environment', config)
lambda_config = get_config_value('aws.lambda', config)
load_balancer_config = get_config_value('aws.load_balancer', config)
s3_config = get_config_value('aws.s3', config)
sns_config = get_config_value('aws.sns', config)
step_functions_config = get_config_value('aws.step_functions', config)
vpc_config = get_config_value('aws.vpc', config)

app = cdk.App()
s3_bucket_stack = S3BucketStack(app, '-'.join([project, environment, 's3']), s3_config, env=aws_environment)
vpc_stack = VPCStack(app, '-'.join([project, environment, 'vpc']), vpc_config, env=aws_environment)
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']), env=aws_environment)
lambda_stack = LambdaStack(
    app, '-'.join([project, environment, 'lambda']), lambda_config, vpc=vpc_stack.vpc, env=aws_environment
)
step_functions_stack = StepFunctionsStack(
    app, '-'.join([project, environment, 'stepfunctions']), step_functions_config, env=aws_environment
)
sns_stack = SNSStack(app, '-'.join([project, environment, 'sns']), sns_config, env=aws_environment)
date_now = datetime.datetime.now().strftime("%Y%m%d")
load_balancer_stack = LoadBalancerStack(
    app, '-'.join([project, environment, 'lb']),
    load_balancer_config=load_balancer_config,
    vpc=vpc_stack.vpc,
    bucket_name=get_config_value('bucket.name', s3_config),
    keypair_name=Keypair.create_keypair(
        keypair_name='-'.join([project, environment, date_now, 'key']), aws_tags=aws_tags_list
    ),
    env=aws_environment
)
step_functions_stack.add_dependency(lambda_stack)
step_functions_stack.add_dependency(sns_stack)
lambda_stack.add_dependency(lambda_layer_stack)
lambda_stack.add_dependency(s3_bucket_stack)
lambda_stack.add_dependency(load_balancer_stack)
load_balancer_stack.add_dependency(s3_bucket_stack)
load_balancer_stack.add_dependency(vpc_stack)
for key, value in aws_tags.items():
    cdk.Tags.of(app).add(key, value or " ", priority=1)
stacks = [s3_bucket_stack, vpc_stack, lambda_layer_stack, lambda_stack, step_functions_stack, sns_stack,
          load_balancer_stack]
for stack in stacks:
    stack_type = type(stack)
    stack_name = stack_type.__name__.partition('Stack')[0]
    cdk.Tags.of(stack).add('Name', '-'.join([stack_name, 'stack', 'for', project]).lower(), priority=2)
    cdk.Tags.of(stack).add('app role', stack_name.lower(), priority=2)
app.synth()
