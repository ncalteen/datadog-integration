from aws_cdk import (
    aws_iam,
    NestedStack
)
from constructs import Construct


class IAMStack(NestedStack):
    """Generates IAM resources for other stacks."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 dd_secret_arn: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM role for various AWS Lambda functions
        self.lambda_role = aws_iam.Role(scope=self,
                                        id='lambda-role',
                                        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                                        description='Lambda role for various demo functions')

        # Add basic AWS Lambda permissions for logging, metrics, etc
        self.lambda_role.add_managed_policy(
            policy=aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'))

        # Add permissions to invoke Lambda functions (for the REST API)
        self.lambda_role.add_managed_policy(
            policy=aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaRole'))

        # Add permissions to read/write the DynamoDB timestamp table
        self.lambda_role.attach_inline_policy(
            policy=aws_iam.Policy(scope=self,
                                  id='dynamodb-policy',
                                  statements=[
                                      aws_iam.PolicyStatement(
                                          actions=[
                                              'dynamodb:DeleteItem',
                                              'dynamodb:DescribeTable',
                                              'dynamodb:GetItem',
                                              'dynamodb:GetRecords',
                                              'dynamodb:ListTables',
                                              'dynamodb:PutItem',
                                              'dynamodb:Query',
                                              'dynamodb:Scan',
                                              'dynamodb:UpdateItem'
                                          ],
                                          effect=aws_iam.Effect.ALLOW,
                                          resources=['*'])]))

        # Add permissions to get the Datadog secret
        self.lambda_role.attach_inline_policy(
            policy=aws_iam.Policy(scope=self,
                                  id='datadog-secret-policy',
                                  statements=[
                                      aws_iam.PolicyStatement(
                                          actions=[
                                              'secretsmanager:DescribeSecret',
                                              'secretsmanager:GetSecretValue'
                                          ],
                                          effect=aws_iam.Effect.ALLOW,
                                          resources=[dd_secret_arn])]))
