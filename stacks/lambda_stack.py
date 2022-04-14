import os

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_lambda as _lambda,
    core as cdk
)


class LambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket_name = cdk.Fn.import_value(
            construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'S3BucketName'
        )
        load_balancer_dns = cdk.Fn.import_value(
            construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'LbDnsName'
        )

        publish_logs_policy_name = '-'.join([construct_id, 'publish logs to cloudwatch policy'.replace(' ', '-')])
        publish_logs_policy = iam.ManagedPolicy(
            self, 'PublishLogsToCloudwatchPolicy',
            managed_policy_name=publish_logs_policy_name,
            description='Policy to publish logs to Cloudwatch',
            statements=[
                iam.PolicyStatement(
                    sid='AllowPublishLogsToCloudwatch',
                    actions=[
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:PutLogEvents'
                    ],
                    resources=['arn:aws-cn:logs:*:*:*']
                )
            ]
        )
        download_upload_s3_policy_name = '-'.join([construct_id, 'download upload s3 object policy'.replace(' ', '-')])
        download_upload_s3_policy = iam.ManagedPolicy(
            self, 'DownloadUploadS3ObjectPolicy',
            managed_policy_name=download_upload_s3_policy_name,
            description='Policy to download and upload objects in S3 bucket',
            statements=[
                iam.PolicyStatement(
                    sid='AllowListOfSpecificBucket',
                    actions=['s3:ListBucket'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                ),
                iam.PolicyStatement(
                    sid='AllowGetObjectOfSpecificBucket',
                    actions=['s3:GetObject'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                ),
                iam.PolicyStatement(
                    sid='AllowPutObjectOfSpecificBucket',
                    actions=['s3:PutObject'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                )
            ]
        )
        delete_s3_policy_name = '-'.join([construct_id, 'delete s3 object policy'.replace(' ', '-')])
        delete_s3_policy = iam.ManagedPolicy(
            self, 'DeleteS3ObjectPolicy',
            managed_policy_name=delete_s3_policy_name,
            description='Policy to delete objects in S3 bucket',
            statements=[
                iam.PolicyStatement(
                    sid='AllowDeleteObjectOfSpecificBucket',
                    actions=['s3:DeleteObjectVersion', 's3:DeleteObject'],
                    resources=[
                        'arn:aws-cn:s3:::' + s3_bucket_name,
                        'arn:aws-cn:s3:::' + s3_bucket_name + '/*'
                    ]
                )
            ]
        )
        test_website_lambda_role_name = '-'.join([construct_id, 'test website role'.replace(' ', '-')])
        test_website_lambda_role = iam.Role(
            self, 'TestWebsiteLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for test website Lambda function",
            managed_policies=[
                publish_logs_policy,
                download_upload_s3_policy
            ],
            role_name=test_website_lambda_role_name,
        )

        generate_report_lambda_role_name = '-'.join([construct_id, 'generate report role'.replace(' ', '-')])
        generate_report_lambda_role = iam.Role(
            self, 'GenerateReportLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for generate report Lambda function",
            managed_policies=[
                publish_logs_policy,
                download_upload_s3_policy,
                delete_s3_policy
            ],
            role_name=generate_report_lambda_role_name,
        )

        parse_report_lambda_role_name = '-'.join([construct_id, 'parse report role'.replace(' ', '-')])
        parse_report_lambda_role = iam.Role(
            self, 'ParseReportLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for parse report Lambda function",
            managed_policies=[
                publish_logs_policy,
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole')
            ],
            role_name=parse_report_lambda_role_name,
        )

        test_website_lambda_function_name = '-'.join([construct_id, 'test website function'.replace(' ', '-')])
        test_website_lambda_function = _lambda.Function(
            self, 'TestWebsiteLambda',
            code=_lambda.Code.from_asset(path=os.path.join(os.path.dirname(__file__), '..', 'lambda', 'test_website')),
            handler="test_website.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            description='Lambda function to execute website tests',
            environment={
                's3_bucket_name': s3_bucket_name
            },
            function_name=test_website_lambda_function_name,
            layers=[
                _lambda.LayerVersion.from_layer_version_arn(
                    self, 'PytestLayer', layer_version_arn=cdk.Fn.import_value(
                        construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'PytestLayerArn'
                    )
                ),
                _lambda.LayerVersion.from_layer_version_arn(
                    self, 'SeleniumLayer', layer_version_arn=cdk.Fn.import_value(
                        construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'SeleniumLayerArn'
                    )
                ),
                _lambda.LayerVersion.from_layer_version_arn(
                    self, 'ChromedriverLayer', layer_version_arn=cdk.Fn.import_value(
                        construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'ChromedriverLayerArn'
                    )
                )
            ],
            memory_size=10240,
            role=test_website_lambda_role,
            timeout=cdk.Duration.seconds(900)
        )
        test_website_lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        generate_report_lambda_function_name = '-'.join([construct_id, 'generate report function'.replace(' ', '-')])
        generate_report_lambda_function = _lambda.Function(
            self, 'GenerateReportLambda',
            code=_lambda.Code.from_asset(
                path=os.path.join(os.path.dirname(__file__), '..', 'lambda', 'generate_report')
            ),
            handler="generate_report.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            description='Lambda function to generate allure report',
            environment={
                's3_bucket_name': s3_bucket_name
            },
            function_name=generate_report_lambda_function_name,
            layers=[
                _lambda.LayerVersion.from_layer_version_arn(
                    self, 'AllureLayer', layer_version_arn=cdk.Fn.import_value(
                        construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'AllureLayerArn'
                    )
                )
            ],
            memory_size=4096,
            role=generate_report_lambda_role,
            timeout=cdk.Duration.seconds(900)
        )
        generate_report_lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        parse_report_sg_name = '-'.join([construct_id, 'parse report sg'.replace(' ', '-')])
        parse_report_sg = ec2.SecurityGroup(
            self, 'ParseReportLambdaSecurityGroup', vpc=vpc,
            description='Security group for parse report lambda',
            security_group_name=parse_report_sg_name
        )
        parse_report_sg.add_egress_rule(
            peer=ec2.Peer.ipv4('0.0.0.0/0'),
            connection=ec2.Port.all_traffic(),
            description='internet'
        )
        parse_report_lambda_function_name = '-'.join([construct_id, 'parse report function'.replace(' ', '-')])
        parse_report_lambda_function = _lambda.Function(
            self, 'ParseReportLambda',
            code=_lambda.Code.from_asset(path=os.path.join(os.path.dirname(__file__), '..', 'lambda', 'parse_report')),
            handler="parse_report.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            description='Lambda function to parse tests result',
            environment={
                'allure_report_endpoint': load_balancer_dns
            },
            function_name=parse_report_lambda_function_name,
            memory_size=4096,
            role=parse_report_lambda_role,
            security_groups=[parse_report_sg],
            timeout=cdk.Duration.seconds(900),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE).subnets)
        )
        parse_report_lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        cdk.Tags.of(test_website_lambda_role).add('Name', test_website_lambda_role_name.lower(), priority=50)
        cdk.Tags.of(generate_report_lambda_role).add('Name', generate_report_lambda_role_name.lower(), priority=50)
        cdk.Tags.of(parse_report_lambda_role).add('Name', parse_report_lambda_role_name.lower(), priority=50)
        cdk.Tags.of(test_website_lambda_function).add('Name', test_website_lambda_function_name.lower(), priority=50)
        cdk.Tags.of(generate_report_lambda_function).add(
            'Name', generate_report_lambda_function_name.lower(), priority=50
        )
        cdk.Tags.of(parse_report_lambda_function).add('Name', parse_report_lambda_function_name.lower(), priority=50)
        cdk.Tags.of(parse_report_sg).add('Name', parse_report_sg_name.lower(), priority=50)

        cdk.CfnOutput(self, 'OutputTestWebsiteLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'TestWebsiteLambdaArn',
                      value=test_website_lambda_function.function_arn)
        cdk.CfnOutput(self, 'OutputGenerateReportLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'GenerateReportLambdaArn',
                      value=generate_report_lambda_function.function_arn)
        cdk.CfnOutput(self, 'OutputParseReportLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'ParseReportLambdaArn',
                      value=parse_report_lambda_function.function_arn)
