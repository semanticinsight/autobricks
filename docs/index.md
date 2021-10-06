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

This library supports all by simply setting the following environment variables as required for each method. 
The AUTH_TYPE sets the authorisation mode and therefore what configuration to expect. 
Ensure that sensitive values are managed using secret redaction e.g. key vault or some other method.


| Variable              | User PAT | SP                  | SP on Mgmt Endpoint               |
|-----------------------|----------|---------------------|-----------------------------------|
|AUTH_TYPE              | USER     | SERVICE_PRINCIPLE   | SERVICE_PRINCIPLE_MGMT_ENDPOINT   |
|DBUTILSTOKEN           | &#10003; | &#10003;            | &#10003;                          |
|TENANT_ID              |          | &#10003;            | &#10003;                          |
|SP_CLIENT_ID           |          | &#10003;            | &#10003;                          |
|SP_CLIENT_SECRET       |          | &#10003;            | &#10003;                          |
|AD_RESOURCE            |          | &#10003;            | &#10003;                          |
|MGMT_RESOURCE_ENDPOINT |          |                     | &#10003;                          |
|WORKSPACE_NAME         |          |                     | &#10003;                          | 
|RESOURCE_GROUP         |          |                     | &#10003;                          |
|SUBSCRIPTION_ID        |          |                     | &#10003;                          |
|DATABRICKS_API_HOST    | &#10003; | &#10003;            | &#10003;                          |

Also note that library will use simple rest calls to retrieve tokens. An alternative approach 
is to leverage the adal library to authenticate. If you wish to authenticate over [adal](https://pypi.org/project/adal/) please
refer to following settings:

| Variable              | SP                     | SP on Mgmt Endpoint                  |
|-----------------------|------------------------|--------------------------------------|
|AUTH_TYPE              | SERVICE_PRINCIPLE_ADAL | SERVICE_PRINCIPLE_MGMT_ENDPOINT_ADAL |
|DBUTILSTOKEN           | &#10003;               | &#10003;                             |
|TENANT_ID              | &#10003;               | &#10003;                             |
|SP_CLIENT_ID           | &#10003;               | &#10003;                             |
|SP_CLIENT_SECRET       | &#10003;               | &#10003;                             |
|AD_RESOURCE            | &#10003;               | &#10003;                             |
|MGMT_RESOURCE_ENDPOINT |                        | &#10003;                             |
|WORKSPACE_NAME         |                        | &#10003;                             | 
|RESOURCE_GROUP         |                        | &#10003;                             |
|SUBSCRIPTION_ID        |                        | &#10003;                             |
|DATABRICKS_API_HOST    | &#10003;               | &#10003;                             |

When deciding between [adal](https://pypi.org/project/adal/) and rest calls the following is relevant:
- [adal](https://pypi.org/project/adal/) may not work in Azure DevOps in highly restricted private network setups
- Rest calls are more simple however if MS makes any changes to the API's the [adal](https://pypi.org/project/adal/) isn't there to abstract those changes.

The following variables will default.

| Variable              | Default                              |
|-----------------------|--------------------------------------|
|AUTH_TYPE              | SERVICE_PRINCIPLE                    |
|AD_RESOURCE            | 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d |
|MGMT_RESOURCE_ENDPOINT | https://management.core.windows.net/ |



## Modules

The following modules provide high level functions that can be used to python script management and deploy assets to databricks workspaces:

- autobricks.Cluster
- autobricks.Dbfs
- autobricks.Job
- autobricks.Library
- autobricks.Workspace

