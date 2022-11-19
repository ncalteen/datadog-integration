from aws_cdk import (
    aws_apigateway,
    aws_lambda_python_alpha as aws_lambda_python,
    NestedStack
)
from constructs import Construct


class APIStack(NestedStack):
    """Implements a simple REST API."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 api_function: aws_lambda_python.PythonFunction,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # REST API to receive incoming requests
        self.rest_api = aws_apigateway.LambdaRestApi(scope=self,
                                                     id='rest-api',
                                                     description='Invokes a random function',
                                                     deploy=True,
                                                     handler=api_function,
                                                     proxy=True,
                                                     binary_media_types=['application/json'])
