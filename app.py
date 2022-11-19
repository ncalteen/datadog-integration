#!/usr/bin/env python3
import aws_cdk as cdk

from datadog_cdk.datadog_integ_stack import DatadogIntegStack
from datadog_cdk.datadog_cdk_stack import DatadogCdkStack

# DatadogCdkStack requires an ARN to the AWS Secrets Manager secret
# containing the API key used to authenticate to Datadog
dd_secret_arn = 'arn:aws:secretsmanager:us-east-1:123506179955:secret:datadog_credentials-FroCM0'

# This value isn't a secret
dd_site = 'datadoghq.com'

# Used in the trust policy for the Datadog <-> AWS integration
dd_external_id = '8223bf1c86c3463cbf733f34d1675446'

app = cdk.App()

# AWS <-> Datadog integration role
DatadogIntegStack(
    scope=app,
    construct_id='DatadogIntegStack',
    dd_external_id=dd_external_id)

# Demo infrastructure
DatadogCdkStack(
    scope=app,
    construct_id='DatadogCdkStack',
    dd_secret_arn=dd_secret_arn,
    dd_site=dd_site)

app.synth()
