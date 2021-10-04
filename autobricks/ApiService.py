import requests
from requests.exceptions import HTTPError
from enum import Enum
import logging
from typing import Union
from .AuthFactory import auth_factory, AuthenticationType
from .Auth import Auth


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")


API_VERSION = "2.0"


class ApiService:

    def __init__(self, configuration:dict):

        auth_type_str = configuration["auth_type"]
        self.host = configuration["databricks_api_host"]
        auth_type:AuthenticationType = AuthenticationType[auth_type_str]
        auth: Auth = auth_factory.get_auth(auth_type, configuration)
        
        self._headers = auth.get_headers()


    def _base_api_get(self, url: str, headers: dict, data: dict = None, query: str = None):

        if query:
            url = f"{url}?{query}"
        response = requests.get(url=url, headers=headers, json=data)

        try:
            response.raise_for_status()

        except HTTPError as e:

            msg = f"{e.response.status_code} error at {url} {e.response.text}"
            logger.error(msg)
            raise e

        return response


    def _base_api_post(self, url: str, headers: dict, data:Union[str,dict]):

        response = requests.post(url=url, headers=headers, json=data)
        
        try:
            response.raise_for_status()

        except HTTPError as e:

            msg = f"{e.response.status_code} error at {url} {e.response.text}"
            logger.error(msg)
            raise e

        return response


    def api_get(self, api: str, function: str, data: dict = None, query: str = None):

        url = f"{self.host}/api/{API_VERSION}/{api}/{function}"
        if query:
            url = f"{url}?{query}"
        response = self._base_api_get(url=url, headers=self._headers, data=data)

        return response.json()


    def api_post(self, api: str, function: str, data: dict):

        url = f"{self.host}/api/{API_VERSION}/{api}/{function}"
        response = self._base_api_post(url=url, headers=self._headers, data=data)

        return response.json()