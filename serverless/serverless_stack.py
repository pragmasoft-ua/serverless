from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_assets as s3_assets
)


class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket: s3.Bucket = s3.Bucket(self, 'arium-serverless-data-bucket', block_public_access=s3.BlockPublicAccess.BLOCK_ALL, encryption=s3.BucketEncryption.S3_MANAGED)

        layer = _lambda.LayerVersion.from_layer_version_arn(self, 'AWSLambda-Python37-SciPy1x', 'arn:aws:lambda:us-east-1:668099181075:layer:AWSLambda-Python37-SciPy1x:22')

        # The code that defines your stack goes here
        my_lambda = _lambda.Function(self, 'HelloHandler', runtime=_lambda.Runtime.PYTHON_3_7,
                                     code=_lambda.Code.asset('lambda'), handler='hello.handler', environment={'DATA_BUCKET' : bucket.bucket_name})

        my_lambda.add_layers(layer)

        bucket.grant_read_write(my_lambda)


