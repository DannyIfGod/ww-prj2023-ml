import json

# get_info() function that returns the service info
def get_info():
    data = {
        "app": 'my-service',
        "version": 1
    }
    return json.dumps(data)
