import json
import numpy as np

def handler(event, context):
    '''
    AWS Lambda handler
    '''
    print(f'request: {json.dumps(event)}')
    np.random.seed(1000)
    array = np.random.randint(0,100,100)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Hello, CDK! You have hit {event["path"]}',
        'array': array.tolist()
    }

