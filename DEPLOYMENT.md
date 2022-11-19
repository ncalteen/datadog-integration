# Deployment

The following sections outline the steps to deploy the demo application to your own AWS account.

## Prerequisites

In order to run this project, you will need the following. Links to the steps to fulfill each are included.

* [Node.js and NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm#using-a-node-version-manager-to-install-nodejs-and-npm)
* [An active AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
* [Docker Desktop](https://docs.docker.com/desktop/)
* [Datadog CLI](https://www.npmjs.com/package/@datadog/cli)

## Step 1: Install the AWS integration in your Datadog account

When installing the AWS integration, you will be given an `externalId` that is needed as part of the AWS CDK app.

1. Install the [AWS Datadog integration](https://app.datadoghq.com/integrations/amazon-web-services/landing)
2. [Generate the external ID](https://docs.datadoghq.com/integrations/guide/aws-manual-setup/?tab=roledelegation#generate-an-external-id)
3. Save the external ID for the following steps

## Step 2: Bootstrap your AWS account

If you have not already done so, you will need to bootstrap your account with the AWS CDK.

1. Follow the instructions [here](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_bootstrap) to boostrap your account

## Step 3: Set up the AWS CDK app

Next, you can clone this repository and set up the CDK app.

1. Clone this repository to your workstation

   ```bash
   git clone https://github.com/ncalteen/datadog_integration
   ```

1. Install the CDK app's dependencies

   ```bash
   cd datadog_integration
   pip install -r requirements.txt
   ```

1. Open [./app.py](./app.py)
1. On each of the following lines, change the listed value

   | Line Number | Variable name    | Replace with...                                  |
   |-------------|------------------|--------------------------------------------------|
   | 9           | `dd_secret_arn`  | ARN of the **`DD_API_KEY`** secret you created   |
   | 12          | `dd_site`        | Site name for your Datadog integration           |
   | 15          | `dd_external_id` | External ID for your AWS <-> Datadog integration |

1. Save your changes

### Step 4: Deploy the CDK app

In this step, you will deploy your CDK app to your AWS account.

1. Run the following command from the command line or terminal from within the `datadog_integration` repository (make sure to change the output path to a path on your workstation)

    ```bash
    cdk deploy --outputs-file /path/to/cdk-outputs.json 
    ```

1. Confirm that the CDK will create the listed resources

### Step 6: Verify

As a final step, you will verify that data is coming into Datadog from your AWS account.

**Note:** It can take 15-20 minutes for initial data to come from AWS to Datadog.
