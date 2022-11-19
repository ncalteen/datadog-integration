from aws_cdk import (
    aws_dynamodb,
    NestedStack,
    RemovalPolicy
)
from constructs import Construct


class DynamoDBStack(NestedStack):
    """Implements a DynamoDB table for timestamps and junk data."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.timestamp_db = aws_dynamodb.Table(
            scope=self,
            id='timestamp-db',
            removal_policy=RemovalPolicy.DESTROY,
            partition_key=aws_dynamodb.Attribute(name='uuid',
                                                 type=aws_dynamodb.AttributeType.STRING))
