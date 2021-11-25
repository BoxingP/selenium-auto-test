from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    core as cdk
)


class LambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, lambda_layers: list, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = iam.Role(
            self, 'LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
            description="IAM role for Lambda function",
            managed_policies=[],
            role_name='-'.join([construct_id, 'role'.replace(' ', '-')]),
        )

        lambda_function = _lambda.Function(
            self, 'LambdaFunction',
            code=_lambda.Code.from_asset(path="./selenium_auto_test/lambda"),
            handler="test_website.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_6,
            layers=lambda_layers,
            memory_size=4096,
            role=lambda_role,
            timeout=cdk.Duration.seconds(900)

        )
        lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
