from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    core as cdk
)


class LambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket_name = cdk.Fn.import_value(
            construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'S3BucketName'
        )

        publish_logs_to_cloudwatch = iam.ManagedPolicy(self, 'PublishLogsPolicy',
                                                       managed_policy_name='-'.join(
                                                           [construct_id, 'publish logs policy'.replace(' ', '-')]
                                                       ),
                                                       description='Policy to operate EC2 instances',
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
        operating_s3_policy = iam.ManagedPolicy(self, 'OperatingS3Policy',
                                                managed_policy_name='-'.join(
                                                    [construct_id, 'operating s3 policy'.replace(' ', '-')]
                                                ),
                                                description='Policy to operate S3 bucket',
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
        deleting_s3_object_policy = iam.ManagedPolicy(self, 'DeletingS3ObjectPolicy',
                                                      managed_policy_name='-'.join(
                                                          [construct_id, 'deleting s3 object policy'.replace(' ', '-')]
                                                      ),
                                                      description='Policy to delete S3 object',
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
        test_website_lambda_role = iam.Role(
            self, 'TestWebsiteLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for Lambda function",
            managed_policies=[
                publish_logs_to_cloudwatch,
                operating_s3_policy
            ],
            role_name='-'.join([construct_id, 'test website role'.replace(' ', '-')]),
        )

        generate_report_lambda_role = iam.Role(
            self, 'GenerateReportLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for Lambda function",
            managed_policies=[
                publish_logs_to_cloudwatch,
                operating_s3_policy,
                deleting_s3_object_policy
            ],
            role_name='-'.join([construct_id, 'generate report role'.replace(' ', '-')]),
        )

        parse_report_lambda_role = iam.Role(
            self, 'ParseReportLambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for Lambda function",
            managed_policies=[
                publish_logs_to_cloudwatch
            ],
            role_name='-'.join([construct_id, 'parse report role'.replace(' ', '-')]),
        )

        test_website_lambda_function = _lambda.Function(
            self, 'TestWebsiteLambda',
            code=_lambda.Code.from_asset(path="./lambda/test_website"),
            handler="test_website.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            environment={
                's3_bucket_name': s3_bucket_name
            },
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
            memory_size=4096,
            role=test_website_lambda_role,
            timeout=cdk.Duration.seconds(900)
        )
        test_website_lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        generate_report_lambda_function = _lambda.Function(
            self, 'GenerateReportLambda',
            code=_lambda.Code.from_asset(path="./lambda/generate_report"),
            handler="generate_report.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            environment={
                's3_bucket_name': s3_bucket_name
            },
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

        parse_report_lambda_function = _lambda.Function(
            self, 'ParseReportLambda',
            code=_lambda.Code.from_asset(path="./lambda/parse_report"),
            handler="parse_report.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            memory_size=4096,
            role=parse_report_lambda_role,
            timeout=cdk.Duration.seconds(900)
        )
        parse_report_lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        cdk.CfnOutput(self, 'OutputTestWebsiteLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'TestWebsiteLambdaArn',
                      value=test_website_lambda_function.function_arn)
        cdk.CfnOutput(self, 'OutputGenerateReportLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'GenerateReportLambdaArn',
                      value=generate_report_lambda_function.function_arn)
        cdk.CfnOutput(self, 'OutputParseReportLambdaArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'ParseReportLambdaArn',
                      value=parse_report_lambda_function.function_arn)
