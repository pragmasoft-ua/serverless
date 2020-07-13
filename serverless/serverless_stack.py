from aws_cdk import (
    core,
    aws_lambda as _lambda
)


class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        layer = _lambda.LayerVersion.from_layer_version_arn(self, 'AWSLambda-Python37-SciPy1x', 'arn:aws:lambda:us-east-1:668099181075:layer:AWSLambda-Python37-SciPy1x:22')

        # The code that defines your stack goes here
        my_lambda = _lambda.Function(self, 'HelloHandler', runtime=_lambda.Runtime.PYTHON_3_7,
                                     code=_lambda.Code.asset('lambda'), handler='hello.handler')

        my_lambda.add_layers(layer)
