import os

from aws_cdk import (
    aws_lambda as _lambda,
    core as cdk
)


class LambdaLayerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pytest_layer = _lambda.LayerVersion(
            self, 'PytestLayer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'pytest')),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        selenium_layer = _lambda.LayerVersion(
            self, 'SeleniumLayer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'selenium')),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        chromedriver_layer = _lambda.LayerVersion(
            self, 'ChromedriverLayer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'chromedriver')),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        allure_layer = _lambda.LayerVersion(
            self, 'AllureLayer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'allure')),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        psycopg2_layer = _lambda.LayerVersion(
            self, 'Psycopg2Layer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'psycopg2')),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        sqlalchemy_layer = _lambda.LayerVersion(
            self, 'SqlalchemyLayer',
            code=_lambda.Code.from_asset(os.path.join(os.path.abspath(os.sep), 'tmp', 'sqlalchemy')),
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
        cdk.CfnOutput(self, 'OutputPsycopg2LayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'Psycopg2LayerArn',
                      value=psycopg2_layer.layer_version_arn)
        cdk.CfnOutput(self, 'OutputSqlalchemyLayerArn',
                      export_name=construct_id.rsplit('-', 1)[0].title().replace('-', '') + 'SqlalchemyLayerArn',
                      value=sqlalchemy_layer.layer_version_arn)
