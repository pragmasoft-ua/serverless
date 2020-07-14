import json
import numpy as np
import boto3
import boto3_type_annotations.s3 as s3
import os

s3_client: s3.Client = None

def handler(event, context):
    '''
    AWS Lambda handler
    '''
    print(f'request: {json.dumps(event)}')
    arr = np.random.randint(0,100,100)
    file_name = '/tmp/rand.npy'
    np.save(file_name, arr)
    global s3_client
    if s3_client is None:
        s3_client = boto3.client('s3')
        np.random.seed(1000)
    bucket_name = os.environ['DATA_BUCKET']
    print(f'save to bucket {bucket_name}')
    s3_client.upload_file(file_name, bucket_name, 'rand.npy')
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Hello, CDK! You have hit {event["path"]}',
        'array': arr.tolist()
    }

def init_s3_client():
    return s3_client

