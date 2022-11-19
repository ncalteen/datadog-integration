from aws_cdk import (
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_lambda_python_alpha as aws_lambda_python,
    Duration,
    Stack
)
from constructs import Construct
from datadog_cdk_constructs_v2 import Datadog

from .stacks import (
    APIStack,
    DynamoDBStack,
    IAMStack,
    LambdaStack
)


class DatadogCdkStack(Stack):
    """Implements the demo infrastructure."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 dd_secret_arn: str,
                 dd_site: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM resources
        self.iam_stack = IAMStack(scope=self,
                                  construct_id='iam-stack',
                                  dd_secret_arn=dd_secret_arn)

        # DynamoDB resources
        self.dynamodb_stack = DynamoDBStack(scope=self,
                                            construct_id='dynamodb-stack')

        # Lambda resources
        self.lambda_stack = LambdaStack(scope=self,
                                        construct_id='lambda-stack',
                                        dynamodb_table_name=self.dynamodb_stack.timestamp_db.table_name,
                                        iam_role=self.iam_stack.lambda_role)

        # API Gateway resources
        self.api_stack = APIStack(scope=self,
                                  construct_id='api-stack',
                                  api_function=self.lambda_stack.api_handler_function)

        # Demonstrates calling the REST API
        # This has to be created after the Lambda stack to avoid circular dependencies
        self.api_caller_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='api-caller-function',
            entry='lambda',
            index='api_caller.py',
            handler='lambda_handler',
            function_name='APICallerFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Calls the REST API',
            role=self.iam_stack.lambda_role,
            timeout=Duration.seconds(5),
            environment={
                'API': self.api_stack.rest_api.url
            })
        
        # Schedule the function to run every minute
        self.api_invoke_rule = aws_events.Rule(
            scope=self,
            id='api-invoke-rule',
            schedule=aws_events.Schedule.rate(duration=Duration.minutes(1)))
        self.api_invoke_rule.add_target(
            target=aws_events_targets.LambdaFunction(self.api_caller_function))

        # Add Datadog
        datadog = Datadog(scope=self,
                          id='Datadog',
                          python_layer_version=64,
                          extension_layer_version=33,
                          site=dd_site,
                          api_key_secret_arn=dd_secret_arn)
        
        # Add the Datadog layer to the Lambda functions
        datadog.add_lambda_functions(
            lambda_functions=[
                self.lambda_stack.broken_function,
                self.lambda_stack.timeout_function,
                self.lambda_stack.api_handler_function,
                self.lambda_stack.dynamodb_read_function,
                self.lambda_stack.dynamodb_write_function,
                self.api_caller_function
            ])
