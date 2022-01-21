from aws_cdk import (
    aws_lambda as _lambda,
    core as cdk
)


class LambdaLayerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pytest_layer = _lambda.LayerVersion(
            self, 'PytestLayer',
            code=_lambda.Code.from_asset('/tmp/pytest'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        selenium_layer = _lambda.LayerVersion(
            self, 'SeleniumLayer',
            code=_lambda.Code.from_asset('/tmp/selenium'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        chromedriver_layer = _lambda.LayerVersion(
            self, 'ChromedriverLayer',
            code=_lambda.Code.from_asset('/tmp/chromedriver'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        allure_layer = _lambda.LayerVersion(
            self, 'AllureLayer',
            code=_lambda.Code.from_asset('/tmp/allure'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        cdk.CfnOutput(self, 'OutputPytestLayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'PytestLayerArn',
                      value=pytest_layer.layer_version_arn)
        cdk.CfnOutput(self, 'OutputSeleniumLayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'SeleniumLayerArn',
                      value=selenium_layer.layer_version_arn)
        cdk.CfnOutput(self, 'OutputChromedriverLayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'ChromedriverLayerArn',
                      value=chromedriver_layer.layer_version_arn)
        cdk.CfnOutput(self, 'OutputAllureLayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'AllureLayerArn',
                      value=allure_layer.layer_version_arn)
