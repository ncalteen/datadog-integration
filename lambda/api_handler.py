import boto3
import json
import os
import random

from typing import Dict

# Run these outside the handler, since they only
#   needs to run in the Lambda container once.
lambda_client = boto3.client('lambda')

functions = [
    os.environ.get('BROKEN_FUNCTION'),
    os.environ.get('TIMEOUT_FUNCTION'),
    os.environ.get('DDB_WRITE_FUNCTION'),
    os.environ.get('DDB_READ_FUNCTION')
]

def lambda_handler(event: Dict, context: Dict) -> Dict:
    """
    Amazon API Gateway proxies requests to the REST endpoint
        directly to this function (regardless of resource and
        method).

    The payload doesn't matter. This will just invoke one of
    the functions in the stack randomly.
    
    Args:
        event: The input event from API Gateway
        context: The Lambda function context
    
    Returns:
        An API Gateway-formatted response
    """
    function = functions[random.randint(0, len(functions) - 1)]
    
    response = lambda_client.invoke(
        FunctionName=functions[random.randint(0, len(functions) - 1)],
        InvocationType='Event',
        Payload='{}'
    )
    
    print(f'Invoked {function}')
    print(response)
    
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "Status": "OK"
        })
    }