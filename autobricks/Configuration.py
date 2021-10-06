import os

"""
Loads the configuration from environment variables.

"""

_user_schema = {
                    "type" : "object",
                    "properties" : {
                        "auth_type" : {"type" : "string"},
                        "dbutilstoken" : {"type" : "string"},
                        "databricks_api_host" : {"type" : "string"},
                    },
                }

_sp_schema = {
                    "type" : "object",
                    "properties" : {
                        "auth_type" : {"type" : "string"},
                        "sp_client_id" : {"type" : "string"},
                        "sp_client_secret" : {"type" : "string"},
                        "ad_resource" : {"type" : "string"},
                        "databricks_api_host" : {"type" : "string"},
                    },
                }

_spme_schema = {
                    "type" : "object",
                    "properties" : {
                        "auth_type" : {"type" : "string"},
                        "sp_client_id" : {"type" : "string"},
                        "sp_client_secret" : {"type" : "string"},
                        "ad_resource" : {"type" : "string"},
                        "tenant_id" : {"type" : "string"},
                        "mgmt_resource_endpoint" : {"type" : "string"},
                        "workspace_name" : {"type" : "string"},
                        "resource_group" : {"type" : "string"},
                        "subscription_id" : {"type" : "string"},
                        "databricks_api_host" : {"type" : "string"},
                    },
                }

config = {
    "dbutilstoken" : os.getenv("DBUTILSTOKEN"),
    "sp_client_id" : os.getenv("SP_CLIENT_ID"),
    "sp_client_secret" : os.getenv("SP_CLIENT_SECRET"),
    "ad_resource" : os.getenv("AD_RESOURCE", "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"),
    "tenant_id" : os.getenv("TENANT_ID"),
    "mgmt_resource_endpoint" : os.getenv("MGMT_RESOURCE_ENDPOINT", "https://management.core.windows.net/"),
    "workspace_name" : os.getenv("WORKSPACE_NAME"),
    "resource_group" : os.getenv("RESOURCE_GROUP"),
    "subscription_id" : os.getenv("SUBSCRIPTION_ID"),
    "auth_type": os.getenv("AUTH_TYPE", "SERVICE_PRINCIPLE"),
    "databricks_api_host": os.getenv("DATABRICKS_API_HOST")
}
