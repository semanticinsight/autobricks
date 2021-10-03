import os

"""
Loads the configuration from environment variables.

"""

config = {
    "dbutilstoken" : os.getenv("DBUTILSTOKEN"),
    "sp_client_id" : os.getenv("SP_CLIENT_ID"),
    "sp_client_secret" : os.getenv("SP_CLIENT_SECRET"),
    "ad_resource" : os.getenv("AD_RESOURCE"),
    "tenant_id" : os.getenv("TENANT_ID"),
    "mgmt_resource_endpoint" : os.getenv("MGMT_RESOURCE_ENDPOINT"),
    "workspace_name" : os.getenv("WORKSPACE_NAME"),
    "resource_group" : os.getenv("RESOURCE_GROUP"),
    "subscription_id" : os.getenv("SUBSCRIPTION_ID"),
    "auth_type": os.getenv("AUTH_TYPE"),
    "databricks_api_host": os.getenv("DATABRICKS_API_HOST")
}

