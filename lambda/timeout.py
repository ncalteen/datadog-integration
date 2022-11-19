import random

from time import sleep
from typing import Dict


def lambda_handler(event: Dict, context: Dict) -> str:
    """Fails...sometimes.
    
    This function does nothing. It either exceeds the
    time limit or returns success.
    
    Args:
        event: The input event
        context: The Lambda function context
    
    Returns:
        'Success!' if it doesn't time out
    """
    
    # Pick a sleep time
    period = random.randint(a=0, b=10)
    
    # Sleep
    sleep(period)
    
    # We might get here...or time out
    return 'Success!'
