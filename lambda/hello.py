import json


def handler(event, context):
    '''
    AWS Lambda handler
    '''
    print(f'request: {json.dumps(event)}')
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Hello, CDK! You have hit {event["path"]}\n'
    }

