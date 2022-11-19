# Architecture

## Demo Infrastructure

The demo environment used in this repo contains the following infrastructure.

| AWS Service | Resource name | Purpose |
|-------------|---------------|---------|
| IAM         | `DatadogIntegrationRole`  | Allows use of the AWS integration for Datadog                                               |
| IAM         | `lambda-role`             | Allows Lambda functions to call various AWS services to generate fake work                  |
| DynamoDB    | `timestamp-db`            | Holds sample data for reading and writing (in this case, junk data to cause throttling)     |
| Lambda      | `broken-function`         | Constantly throws exceptions to use for visualization of function error rates               |
| Lambda      | `timeout-function`        | Intermittently runs over the configured timeout for visualization of time limit error rates |
| Lambda      | `dynamodb-write-function` | Writes large chunks of data to DynamoDB to intermittently cause throttling errors           |
| Lambda      | `dynamodb-read-function`  | Reads large chunks of data from DynamoDB to intermittently cause throttling errors          |
| Lambda      | `api-handler-function`    | Randomly invokes one of the above functions when requests are made to the REST API          |
| API Gateway | `rest-api`                | Receives incoming `GET` requests for visualization of API hits                              |

## AWS Manual Integration

The reason [manual integration via role delegation](https://docs.datadoghq.com/integrations/guide/aws-manual-setup/?tab=roledelegation) was chosen over launching the Datadog-provided AWS CloudFormation template was simply for ease of use in the demo CDK app. The total effort to write a separate CDK stack for this is minimal, but allows long-term ownership of updates to the role used by Datadog.
