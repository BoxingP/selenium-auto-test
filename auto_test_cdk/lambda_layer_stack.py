from aws_cdk import (
    aws_lambda as _lambda,
    core as cdk
)


class LambdaLayerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pytest_layer = _lambda.LayerVersion(
            self, 'Pytest',
            code=_lambda.Code.from_asset('/tmp/pytest'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        pyyaml_layer = _lambda.LayerVersion(
            self, 'Pyyaml',
            code=_lambda.Code.from_asset('/tmp/pyyaml'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        selenium_layer = _lambda.LayerVersion(
            self, 'Selenium',
            code=_lambda.Code.from_asset('/tmp/selenium'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        chromedriver_layer = _lambda.LayerVersion(
            self, 'Chromedriver',
            code=_lambda.Code.from_asset('/tmp/chromedriver'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        allure_layer = _lambda.LayerVersion(
            self, 'Allure',
            code=_lambda.Code.from_asset('/tmp/allure'),
            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64],
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_6
            ],
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        self.layers = [pytest_layer, pyyaml_layer, selenium_layer, chromedriver_layer, allure_layer]
