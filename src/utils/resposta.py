# src/utils/resposta.py
def ok(data):
    return {"statusCode": 200, "body": data}

def created(data):
    return {"statusCode": 201, "body": data}

def not_found(message="Not found"):
    return {"statusCode": 404, "body": {"error": message}}

def bad_request(message="Bad request"):
    return {"statusCode": 400, "body": {"error": message}}
