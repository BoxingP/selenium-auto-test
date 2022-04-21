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
from utils.keypair import Keypair

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r', encoding='UTF-8') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

ami = config['aws_ec2_ami']
aws_environment = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
aws_tags_list = []
for k, v in config['aws_tags'].items():
    aws_tags_list.append({'Key': k, 'Value': v or ' '})
environment = config['environment']
ec2_inbounds = config['aws_ec2_inbounds']
loadbalancer_inbounds = config['aws_loadbalancer_inbounds']
is_versioned = config['aws_s3_versioned']
project = config['project']
sns_subject = config['aws_sns_subject']
sns_topic = config['aws_sns_topic']
subscribers = config['aws_subscribers']
vpc_cidr = config['aws_vpc_cidr']
event_schedule = config['aws_event_schedule']
aws_s3_bucket_name = '-'.join([project, environment, 's3'])
public_dir = config['allure_screenshots_dir']

app = cdk.App()
s3_bucket_stack = S3BucketStack(
    app, '-'.join([project, environment, 's3']),
    bucket_name=aws_s3_bucket_name, is_versioned=is_versioned, public_dir=public_dir, env=aws_environment
)
vpc_stack = VPCStack(app, '-'.join([project, environment, 'vpc']), vpc_cidr, env=aws_environment)
lambda_layer_stack = LambdaLayerStack(app, '-'.join([project, environment, 'layer']), env=aws_environment)
lambda_stack = LambdaStack(app, '-'.join([project, environment, 'lambda']), vpc=vpc_stack.vpc, env=aws_environment)
step_functions_stack = StepFunctionsStack(
    app, '-'.join([project, environment, 'stepfunctions']),
    schedule=event_schedule,
    subject=sns_subject,
    env=aws_environment
)
sns_stack = SNSStack(app, '-'.join([project, environment, 'sns']), sns_topic, subscribers, env=aws_environment)
date_now = datetime.datetime.now().strftime("%Y%m%d")
load_balancer_stack = LoadBalancerStack(
    app, '-'.join([project, environment, 'lb']),
    ami=ami,
    vpc=vpc_stack.vpc,
    bucket_name=aws_s3_bucket_name,
    keypair_name=Keypair.create_keypair(
        keypair_name='-'.join([project, environment, date_now, 'key']), aws_tags=aws_tags_list
    ),
    ec2_inbounds=ec2_inbounds,
    loadbalancer_inbounds=loadbalancer_inbounds,
    env=aws_environment
)
step_functions_stack.add_dependency(lambda_stack)
step_functions_stack.add_dependency(sns_stack)
lambda_stack.add_dependency(lambda_layer_stack)
lambda_stack.add_dependency(s3_bucket_stack)
lambda_stack.add_dependency(load_balancer_stack)
load_balancer_stack.add_dependency(s3_bucket_stack)
load_balancer_stack.add_dependency(vpc_stack)
for key, value in config['aws_tags'].items():
    cdk.Tags.of(app).add(key, value or " ", priority=1)
stacks = [s3_bucket_stack, vpc_stack, lambda_layer_stack, lambda_stack, step_functions_stack, sns_stack,
          load_balancer_stack]
for stack in stacks:
    stack_type = type(stack)
    stack_name = stack_type.__name__.partition('Stack')[0]
    cdk.Tags.of(stack).add('Name', '-'.join([stack_name, 'stack', 'for', project]).lower(), priority=2)
    cdk.Tags.of(stack).add('app role', stack_name.lower(), priority=2)
app.synth()
