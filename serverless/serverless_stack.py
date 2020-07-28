from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_assets as s3_assets,
    aws_s3_notifications as s3n,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_apigateway as apigateway,
    aws_certificatemanager as cert
)
import typing

STAGE_PARAM = 'stage'
PAYLOAD_PARAM = 'payload.$'

class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        numpy_layer = _lambda.LayerVersion.from_layer_version_arn(self, 'AWSLambda-Python37-SciPy1x', 'arn:aws:lambda:us-east-1:668099181075:layer:AWSLambda-Python37-SciPy1x:22')

        libs_layer = _lambda.LayerVersion(self, 'libs', code= _lambda.Code.from_asset('libs'), compatible_runtimes=[_lambda.Runtime.PYTHON_3_7, _lambda.Runtime.PYTHON_3_8] )

        lambda_asset = _lambda.Code.asset('lambda')

        # The code that defines your stack goes here
        calculation_lambda = _lambda.Function(self, 'CalculationHandler', function_name='serverless-calculation', runtime=_lambda.Runtime.PYTHON_3_7,
                                     code=lambda_asset, handler='calculation.handler')

        calculation_lambda.add_layers(numpy_layer, libs_layer)

        bucket: s3.Bucket = s3.Bucket(self, 'arium-serverless-data-bucket', block_public_access=s3.BlockPublicAccess.BLOCK_ALL, encryption=s3.BucketEncryption.S3_MANAGED)

        bucket.grant_read_write(calculation_lambda)

        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(calculation_lambda), s3.NotificationKeyFilter(prefix="in") )

        calculation_lambda.add_environment('DATA_BUCKET',bucket.bucket_name)

        self.init_api_gateway()

        self.init_statemachine(calculation_lambda)

    def init_statemachine(self, lambda_function: _lambda.IFunction):

        # requires explicit cast due to jsii
        invocation: sfn.IStepFunctionsTask = typing.cast(sfn.IStepFunctionsTask, sfn_tasks.InvokeFunction(lambda_function))

        submit_task = sfn.Task(self, "submit_task", task=invocation, parameters={STAGE_PARAM : 'submit', PAYLOAD_PARAM : '$'})

        map_handler = sfn.Task(self, "map_handler", task=invocation)

        map_task = sfn.Map(
            self, "map_task",
            max_concurrency=100,
            parameters={STAGE_PARAM : 'step', PAYLOAD_PARAM : '$$.Map.Item.Value'}
        ).iterator(map_handler)

        reduce_task = sfn.Task(self, "reduce_task", task=invocation, parameters={STAGE_PARAM : 'step', PAYLOAD_PARAM : '$'})
        
        definition = submit_task \
            .next(map_task) \
            .next(reduce_task)

        sfn.StateMachine(
            self, "arium-mapreduce",
            definition=definition
        )

    def init_api_gateway(self):
        inline_handler = """\
import json

def main(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(event)
    }
"""
        handler_code = _lambda.InlineCode(inline_handler)
        self.api_handler = _lambda.Function(self, "ariumApiHandler", function_name="arium_api_handler", code= handler_code, handler='index.main', runtime=_lambda.Runtime.PYTHON_3_7)
        
        api_domain_certificate = cert.Certificate.from_certificate_arn(self, "api_domain_certificate", "arn:aws:acm:us-east-1:488285037276:certificate/94eba0cb-a1a6-4366-9ab4-0d305f0e9e6a",)

        self.api = apigateway.LambdaRestApi(self,"arium", handler = self.api_handler, domain_name = {
            "domain_name": "arium.casualtyanalytics.co.uk",
            "certificate": api_domain_certificate
        })
