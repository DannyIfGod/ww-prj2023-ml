import json

def get_info():
    data = {
        "app": 'my-service',
        "version": 1
    }
    return json.dumps(data)
