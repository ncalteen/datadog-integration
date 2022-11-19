import random

from time import sleep
from typing import Dict


def lambda_handler(event: Dict, context: Dict) -> Dict:
    """Fails spectacularly.

    This function does nothing...it just fails at some point
    a few seconds after invocation.

    Args:
        event: The input event
        context: The Lambda function context

    Returns:
        Nothing
    """
    # Pick a time period to fail
    period = random.randint(a=0, b=10)

    # Wait
    sleep(period)

    # And fail
    raise Exception(f'Task failed successfully after {period} seconds!')
