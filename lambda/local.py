import json

import reducer

response = reducer.calculate(seed=634781, partitions=20)
print(f'response: {json.dumps(response)}')
