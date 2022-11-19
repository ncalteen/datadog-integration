import boto3
import os
import random

from time import sleep
from typing import Dict

# Get the table ARN from the env vars
table_name = os.environ.get('TABLE_NAME')

# Initialize boto3 client outside the handler
# It can be reused between invocations
dynamodb_table = boto3.resource('dynamodb').Table(table_name)


def lambda_handler(event: Dict, context: Dict) -> int:
    """Continuously scans a DynamoDB table.
    
    The goal is to intermittently exceed the RCU.
    
    Args:
        event: The input event
        context: The Lambda function context
    
    Returns:
        Nothing
    """
    
    # Simluate increased duration
    sleep(random.randint(0, 20))

    # Scan the table and all data
    response = dynamodb_table.scan(
        Select='ALL_ATTRIBUTES'
    )
    
    print(f'Scanned and read {len(response.get("Items"))} items!')
    
    return 0
