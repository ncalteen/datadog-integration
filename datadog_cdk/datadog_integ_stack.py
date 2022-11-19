from aws_cdk import (
    aws_iam,
    Stack
)
from constructs import Construct


class DatadogIntegStack(Stack):
    """Implement resources for the AWS to Datadog integration."""

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 dd_external_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Policy needed by Datadog
        self.datadog_policy = aws_iam.Policy(
            scope=self,
            id='datadog-policy',
            document=aws_iam.PolicyDocument(
                statements=[
                    aws_iam.PolicyStatement(
                        actions=[
                            'apigateway:GET',
                            'autoscaling:Describe*',
                            'backup:List*',
                            'budgets:ViewBudget',
                            'cloudfront:GetDistributionConfig',
                            'cloudfront:ListDistributions',
                            'cloudtrail:DescribeTrails',
                            'cloudtrail:GetTrailStatus',
                            'cloudtrail:LookupEvents',
                            'cloudwatch:Describe*',
                            'cloudwatch:Get*',
                            'cloudwatch:List*',
                            'codedeploy:List*',
                            'codedeploy:BatchGet*',
                            'directconnect:Describe*',
                            'dynamodb:List*',
                            'dynamodb:Describe*',
                            'ec2:Describe*',
                            'ecs:Describe*',
                            'ecs:List*',
                            'elasticache:Describe*',
                            'elasticache:List*',
                            'elasticfilesystem:DescribeFileSystems',
                            'elasticfilesystem:DescribeTags',
                            'elasticfilesystem:DescribeAccessPoints',
                            'elasticloadbalancing:Describe*',
                            'elasticmapreduce:List*',
                            'elasticmapreduce:Describe*',
                            'es:ListTags',
                            'es:ListDomainNames',
                            'es:DescribeElasticsearchDomains',
                            'events:CreateEventBus',
                            'fsx:DescribeFileSystems',
                            'fsx:ListTagsForResource',
                            'health:DescribeEvents',
                            'health:DescribeEventDetails',
                            'health:DescribeAffectedEntities',
                            'kinesis:List*',
                            'kinesis:Describe*',
                            'lambda:GetPolicy',
                            'lambda:List*',
                            'logs:DeleteSubscriptionFilter',
                            'logs:DescribeLogGroups',
                            'logs:DescribeLogStreams',
                            'logs:DescribeSubscriptionFilters',
                            'logs:FilterLogEvents',
                            'logs:PutSubscriptionFilter',
                            'logs:TestMetricFilter',
                            'organizations:Describe*',
                            'organizations:List*',
                            'rds:Describe*',
                            'rds:List*',
                            'redshift:DescribeClusters',
                            'redshift:DescribeLoggingStatus',
                            'route53:List*',
                            's3:GetBucketLogging',
                            's3:GetBucketLocation',
                            's3:GetBucketNotification',
                            's3:GetBucketTagging',
                            's3:ListAllMyBuckets',
                            's3:PutBucketNotification',
                            'ses:Get*',
                            'sns:List*',
                            'sns:Publish',
                            'sqs:ListQueues',
                            'states:ListStateMachines',
                            'states:DescribeStateMachine',
                            'support:DescribeTrustedAdvisor*',
                            'support:RefreshTrustedAdvisorCheck',
                            'tag:GetResources',
                            'tag:GetTagKeys',
                            'tag:GetTagValues',
                            'xray:BatchGetTraces',
                            'xray:GetTraceSummaries'
                        ],
                        resources=['*'],
                        effect=aws_iam.Effect.ALLOW
                    )
                ]
            ),
            policy_name='DatadogIntegrationPolicy'
        )

        # Role for Datadog to assume
        self.datadog_role = aws_iam.Role(
            scope=self,
            id='datadog-role',
            assumed_by=aws_iam.AccountPrincipal(account_id='464622532012'),
            external_ids=[dd_external_id],
            role_name='DatadogIntegrationRole'
        )

        # Attach the role policy
        self.datadog_policy.attach_to_role(role=self.datadog_role)
