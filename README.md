# Jenkins pipeline - Create resource in Azure Cloud with Terraform

This example demonstrates how to deploy a storage account in Azure using Terraform templates via Port Actions.

The workflow is executed through a Jenkins pipeline.

## Prerequisites

1. Install the following plugins in Jenkins:
   1. [Azure Credentials](https://plugins.jenkins.io/azure-credentials/) - This plugin provides the `Azure Service Principal` kind in Jenkins Credentials.
   2. [Terraform Plugin](https://plugins.jenkins.io/terraform/)
   3. [Generic Webhook Trigger](https://plugins.jenkins.io/generic-webhook-trigger/)

## Example - creating a storage account

Follow these steps to get started:

1. Create the following as Jenkins Credentials:
    1. Create the Port Credentials using the `Username with password` kind.
        1. `PORT_CLIENT_ID` - Port Client ID [learn more](https://docs.getport.io/build-your-software-catalog/sync-data-to-catalog/api/#get-api-token).
        2. `PORT_CLIENT_SECRET` - Port Client Secret [learn more](https://docs.getport.io/build-your-software-catalog/sync-data-to-catalog/api/#get-api-token).
    2. Create the Azure Credentials using the `Azure Service Principal` kind. You can create a service principal in order to get the Azure credentials using this [guide](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started-cloud-shell-bash?tabs=bash#create-a-service-principal).
        1. `ARM_CLIENT_ID` - Azure Client ID (APP ID) of the application.
        2. `ARM_CLIENT_SECRET` - Azure Client Secret (Password) of the application.
        3. `ARM_SUBSCRIPTION_ID` - Azure Subscription ID.
        4. `ARM_TENANT_ID` - The Azure [Tenant ID](https://learn.microsoft.com/en-us/azure/azure-portal/get-subscription-tenant-id).
    3. `WEBHOOK_TOKEN` - The webhook token so that the job can only be triggered if that token is supplied.

2. Create a Port [blueprint](https://docs.getport.io/build-your-software-catalog/define-your-data-model/setup-blueprint/#what-is-a-blueprint): [Azure Storage Blueprint](./port/blueprint.json)

> Keep in mind this can be any blueprint you would like and this is just an example.

3. Create a Port Action in the [self-service hub](https://app.getport.io/self-serve) using this [JSON](./port/action.json) definition
4. Create the terraform templates in the root of your GitHub repository. You can them in the [terraform](./terraform/) folder:
    1. `main.tf` - This file will contain the resource blocks which define the Storage Account to be created in the Azure cloud and the entity to be createed in Port.
    2. `variables.tf` – This file will contain the variable declarations that will be used in the resource blocks e.g. the port credentials and port run id.
    3. `output.tf` – This file will contain the url of the Storage Account that needs to be generated on successful completion of “apply” operation. This url will be used on creating the Port entity in the `endpoint` property.

> In the `variables.tf`, replace the default `resource_group_name` with your resource group from your Azure account. Check this [guide](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal) to find your resource groups. You may also wish to set the default values of other variables.

5. Create a Jenkins pipeline using the provided [file](./Jenkinsfile):

    1. [Enable webhook trigger for a pipeline](https://docs.getport.io/create-self-service-experiences/setup-backend/jenkins-pipeline/#enabling-webhook-trigger-for-a-pipeline)
    2. [Define variables for a pipeline](https://docs.getport.io/create-self-service-experiences/setup-backend/jenkins-pipeline/#defining-variables): Define the STORAGE_NAME, STORAGE_LOCATION, PORT_RUN_ID and BLUEPRINT_ID variables.
    3. [Token Setup](https://docs.getport.io/create-self-service-experiences/setup-backend/jenkins-pipeline/#token-setup): Define the token to match `JOB_TOKEN` as configured in your Port Action.

    NB: The pipeline includes a post run task of `cleanWs` whose `deleteDirs` parameter means that all generated files and temporary build artifacts will be deleted. Therefore, be sure to either change it or add backend for your terraform state on initialisation.

6. Trigger the action from the [self-service](https://app.getport.io/self-serve) tab of your Port application.
