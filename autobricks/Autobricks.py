import os
from enum import Enum
import Autobricks
import Cluster
import Dbfs
import Job
import Library
import Workspace
import ApiUtilsBasic

from abc import ABC, abstractmethod
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")


class Auth(ABC):

    @abstractmethod
    def __init__(self, parameters:dict):
        pass

    @abstractmethod
    def get_header(self):
        pass


class UserAuth(Auth):

    def __init__(self, parameters:dict):

        self.bearer_token = parameters["sp_client_id"]

    def get_header(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers



class SPAuth(Auth):

    def __init__(self, parameters:dict):

        self.sp_client_id = parameters["sp_client_id"]
        self.sp_client_secret = parameters["sp_client_secret"]
        self.ad_resource = parameters["ad_resource"]

        self._headers = {"Content-Type: application/x-www-form-urlencoded"}
        self._url = "https://login.microsoftonline.com/$tenant_id/oauth2/token"
        ad_auth_data = f"grant_type=client_credentials&client_id={self.sp_client_id}&resource={self.ad_resource}&client_secret={self.sp_client_secret}"
        self.bearer_token = ApiUtilsBasic.api_post(self._url, self._headers, ad_auth_data)

    def get_header(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers



class SPMgmtEndpointAuth(SPAuth):

    def __init__(self, parameters:dict):

        super.__init__(parameters)
        self.mgmt_resource_endpoint = parameters["mgmt_resource_endpoint"]
        self.workspace_name = parameters["workspace_name"]
        self.resource_group = parameters["resource_group"]
        self.subscription_id = parameters["subscription_id"]

        data = f"grant_type=client_credentials&client_id={self.sp_client_id}&resource={self.mgmt_resource_endpoint}&client_secret={self.sp_client_secret}"
        self.resource_mgmt_token = ApiUtilsBasic.api_post(self._url, self._headers, data)


    def get_header(self):
        get_url=f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Databricks/workspaces/{self.workspace_name}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "X-Databricks-Azure-SP-Management-Token": {self.mgmt_access_token},
            "X-Databricks-Azure-Workspace-Resource-Id": {get_url}
            }
        return headers



class AuthenticationType(Enum):

    user = 1
    service_principal = 2
    service_principal_mgmt_endpoint = 3


class Autobricks:

    def __init__(self) -> None:

        self.autobricks = Autobricks
        self.cluster = Cluster
        self.dbfs = Dbfs
        self.job = Job
        self.library = Library
        self.workspace = Workspace
        
        _header_types = {}


