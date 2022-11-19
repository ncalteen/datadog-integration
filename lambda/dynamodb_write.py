import boto3
import os
import random
import uuid

from datetime import datetime
from time import sleep
from typing import Dict

# Get the table ARN from the env vars
table_name = os.environ.get('TABLE_NAME')

# Initialize boto3 client outside the handler
# It can be reused between invocations
dynamodb_table = boto3.resource('dynamodb').Table(table_name)


def lambda_handler(event: Dict, context: Dict) -> int:
    """Writes big, junk records to a DynamoDB table.

    The goal is to intermittently exceed the provisioned WCU.

    Args:
        event: The input event
        context: The Lambda function context

    Returns:
        Nothing
    """

    # Simluate increased runtime
    sleep(random.randint(0, 20))

    # Insert a random UUID and a timestamp
    random_id = str(uuid.uuid4())
    timestamp = datetime.now()

    for x in range(random.randint(1, 25)):
        dynamodb_table.put_item(Item={
                                    'uuid': random_id,
                                    'timestamp': str(timestamp),
                                    'garbage': 'A' * 5000  # Junk data
                                },
                                ReturnValues='NONE',
                                ReturnConsumedCapacity='NONE',
                                ReturnItemCollectionMetrics='NONE')

    print(f'Inserted item with ID {random_id} and timestamp {timestamp}!')

    return 0
