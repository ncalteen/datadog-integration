import os
import requests

from typing import Dict

api_url = os.environ.get('API')


def lambda_handler(event: Dict, context: Dict) -> int:
    """Calls the REST API every minute.

    Args:
        event: The input event from API Gateway
        context: The Lambda function context

    Returns:
        Nothing
    """
    response = requests.get(api_url)

    print(response)

    return 0
