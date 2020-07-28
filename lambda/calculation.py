import json
import types

import reducer

def handler(event, context):
    '''
    AWS Lambda handler
    '''
    print(f'request: {json.dumps(event)}')
    method_name = event.get('stage', 'submit')
    payload = event.get('payload', None)
    state = dispatch(reducer, method_name, payload)
    return state

def dispatch(module: types.ModuleType, method_name: str = 'submit', payload: object = None) -> object:
    m = getattr(reducer, method_name)
    payload = m(payload)
    return payload

