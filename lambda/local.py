import json

import hello

response = hello.handler({ 'path' : '/local'}, {})
print(f'response: {json.dumps(response)}')
