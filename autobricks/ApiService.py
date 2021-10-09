from .AuthFactory import auth_factory, AuthenticationType
from .Auth import Auth
from .BaseApi import base_api_get as _base_api_get, base_api_post as _base_api_post
from . import AutobricksLogging
from .Exceptions import AutbricksConfigurationInvalid

logger = AutobricksLogging.get_logger(__name__)


API_VERSION = "2.0"


class ApiService:
    def __init__(self, configuration: dict):

        try:
            auth_type_str = configuration["auth_type"]
        except KeyError:
            e = AutbricksConfigurationInvalid(
                "auth_type", valid_values=AuthenticationType
            )
            logger.error(e.message)
            raise e

        try:
            self.host = configuration["databricks_api_host"]
        except KeyError:
            e = AutbricksConfigurationInvalid("databricks_api_host")
            logger.error(e.message)
            raise e

        try:
            auth_type: AuthenticationType = AuthenticationType[auth_type_str]
        except:
            e = AutbricksConfigurationInvalid(
                "auth_type", valid_values=AuthenticationType
            )
            logger.error(e.message)
            raise e

        auth: Auth = auth_factory.get_auth(auth_type, configuration)

        self._headers = auth.get_headers()

    def api_get(self, api: str, function: str, data: dict = None, query: str = None):

        url = f"{self.host}/api/{API_VERSION}/{api}/{function}"
        if query:
            url = f"{url}?{query}"
        response = _base_api_get(url=url, headers=self._headers, json=data)

        return response.json()

    def api_post(self, api: str, function: str, data: dict):

        url = f"{self.host}/api/{API_VERSION}/{api}/{function}"
        response = _base_api_post(url=url, headers=self._headers, json=data)

        return response.json()
