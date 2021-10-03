
from abc import ABC, abstractmethod
import logging
import adal


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")


class Auth(ABC):

    @abstractmethod
    def __init__(self, parameters:dict):
        pass

    @abstractmethod
    def get_headers(self):
        pass


class UserAuth(Auth):

    def __init__(self, parameters:dict):

        self.bearer_token = parameters["dbutilstoken"]

    def get_headers(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers



class SPAuth(Auth):

    def __init__(self, parameters:dict):

        self.sp_client_id = parameters["sp_client_id"]
        self.sp_client_secret = parameters["sp_client_secret"]
        self.ad_resource = parameters["ad_resource"]
        self.tenant_id = parameters["tenant_id"]

        self._authority_url = f"https://login.microsoftonline.com/{self.tenant_id}"
        context = adal.AuthenticationContext(self._authority_url)
        response = context.acquire_token_with_client_credentials(
            resource=self.ad_resource,
            client_id=self.sp_client_id,
            client_secret=self.sp_client_secret
        )
        self.bearer_token = response["accessToken"]

    def get_headers(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        return headers



class SPMgmtEndpointAuth(SPAuth):

    def __init__(self, parameters:dict):

        super().__init__(parameters)
        self.mgmt_resource_endpoint = parameters["mgmt_resource_endpoint"]
        self.workspace_name = parameters["workspace_name"]
        self.resource_group = parameters["resource_group"]
        self.subscription_id = parameters["subscription_id"]

        context = adal.AuthenticationContext(self._authority_url)
        response = context.acquire_token_with_client_credentials(
            resource=self.mgmt_resource_endpoint,
            client_id=self.sp_client_id,
            client_secret=self.sp_client_secret
        )
        self.mgmt_access_token = response["accessToken"]


    def get_headers(self):

        url=f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Databricks/workspaces/{self.workspace_name}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "X-Databricks-Azure-SP-Management-Token": self.mgmt_access_token,
            "X-Databricks-Azure-Workspace-Resource-Id": url
        }
        return headers






