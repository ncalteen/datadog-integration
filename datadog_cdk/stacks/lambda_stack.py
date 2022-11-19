from aws_cdk import (
    aws_iam,
    aws_lambda,
    aws_lambda_python_alpha as aws_lambda_python,
    aws_events,
    aws_events_targets,
    Duration,
    NestedStack
)
from constructs import Construct


class LambdaStack(NestedStack):
    """Implements various Lambda functions to generate demo data."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 dynamodb_table_name: str,
                 iam_role: aws_iam.Role,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Demonstrates failing with an exception
        self.broken_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='broken-function',
            entry='lambda',
            index='broken.py',
            handler='lambda_handler',
            function_name='BrokenFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Does nothing, breaks within 10 seconds',
            role=iam_role,
            timeout=Duration.seconds(15))

        # Demonstrates inconsistent time limit exceeded errors
        self.timeout_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='timeout-function',
            entry='lambda',
            index='timeout.py',
            handler='lambda_handler',
            function_name='TimeoutFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Inconsistently exceeds the time limit',
            role=iam_role,
            timeout=Duration.seconds(5))

        # Demonstrates write throttling to DynamoDB
        self.dynamodb_write_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='dynamodb-write-function',
            entry='lambda',
            index='dynamodb_write.py',
            handler='lambda_handler',
            function_name='DynamoDBWriteFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Writes simple records to DynamoDB',
            role=iam_role,
            timeout=Duration.seconds(60),
            environment={
                'TABLE_NAME': dynamodb_table_name
            })

        # Demonstrates read throttling to DynamoDB
        self.dynamodb_read_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='dynamodb-read-function',
            entry='lambda',
            index='dynamodb_read.py',
            handler='lambda_handler',
            function_name='DynamoDBReadFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Reads records from DynamoDB',
            role=iam_role,
            timeout=Duration.seconds(60),
            environment={
                'TABLE_NAME': dynamodb_table_name
            })

        # API Gateway REST API handler
        # Randomly invokes another demo function
        self.api_handler_function = aws_lambda_python.PythonFunction(
            scope=self,
            id='api-handler-function',
            entry='lambda',
            index='api_handler.py',
            handler='lambda_handler',
            function_name='APIHandlerFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            description='Receives requests from API Gateway',
            role=iam_role,
            timeout=Duration.seconds(60),
            environment={
                'BROKEN_FUNCTION': self.broken_function.function_arn,
                'TIMEOUT_FUNCTION': self.timeout_function.function_arn,
                'DDB_WRITE_FUNCTION': self.dynamodb_write_function.function_arn,
                'DDB_READ_FUNCTION': self.dynamodb_read_function.function_arn
            })

        # Schedule the functions to run every minute
        self.function_invoke_rule = aws_events.Rule(
            scope=self,
            id='function-invoke-rule',
            schedule=aws_events.Schedule.rate(duration=Duration.minutes(1)))
        self.function_invoke_rule.add_target(
            target=aws_events_targets.LambdaFunction(self.broken_function))
        self.function_invoke_rule.add_target(
            target=aws_events_targets.LambdaFunction(self.timeout_function))
        self.function_invoke_rule.add_target(
            target=aws_events_targets.LambdaFunction(self.dynamodb_write_function))
        self.function_invoke_rule.add_target(
            target=aws_events_targets.LambdaFunction(self.dynamodb_read_function))
