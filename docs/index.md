# Welcome to Autobricks

Python Azure databricks API wrapper for CI/CD. For when the CLI just doesn't cut it this allows high level python scripting of databricks assets deployments.

The library is a collection of modules functions of similar topology to the [databricks API version 2.0](https://docs.databricks.com/dev-tools/api/latest/index.html)

## Installation

`pip install autobricks`

## Configuration

Azure databricks allows the following authentication methods:

- [Databricks User PAT Token](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/authentication)
- [Azure Service Principal](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/)
- [Azure Service Principal over the Management End Point](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/)

This library supports all by simply setting the following environment variables as required for each method:

| Variable | User PAT | SP | SP on Mgmt Endpoint |
|----------|----------|----|---------------------|
|AUTH_TYPE              | "USER"    | "SERVICE_PRINCIPLE"                    | "SERVICE_PRINCIPLE_MGMT_ENDPOINT" |
|DBUTILSTOKEN           | required  | required                               | required |
|TENANT_ID              |           | required                               | required |
|SP_CLIENT_ID           |           | required                               | required |
|SP_CLIENT_SECRET       |           | required                               | required |
|AD_RESOURCE            |           | "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d" | "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d" |
|MGMT_RESOURCE_ENDPOINT |           |                                        | "https://management.core.windows.net/" |
|WORKSPACE_NAME         |           |                                        | required | 
|RESOURCE_GROUP         |           |                                        | required |
|SUBSCRIPTION_ID        |           |                                        | required |
|DATABRICKS_API_HOST    | required  | required                               | required |

NOTE: AUTH_TYPE sets the authorisation mode and therefore what configuration to expect. Ensure that sensitive values are managed using secret redaction e.g. key vault or some other method.

## Modules

The following modules provide high level functions that can be used to python script management and deploy assets to databricks workspaces:

- autobricks.Cluster
- autobricks.Dbfs
- autobricks.Job
- autobricks.Library
- autobricks.Workspace

