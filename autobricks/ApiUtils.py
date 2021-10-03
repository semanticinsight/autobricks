import requests
from requests.exceptions import HTTPError
import base64
import sys
from enum import Enum
import logging
from typing import Union
from .AuthFactory import auth_factory, AuthenticationType
from .Auth import Auth


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(f"autobricks.ApiUtils")


class OS(Enum):

    WINDOWS = 1
    LINUX = 2
    MAC = 3


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


def base64_decode(base64_string: str, encoding: str = "utf-8"):

    base64_bytes = base64_string.encode(encoding)
    content_bytes = base64.b64decode(base64_bytes)

    return content_bytes


def base64_encode(string_bytes: bytes, ecoding: str = "utf-8"):

    base64_bytes = base64.b64encode(string_bytes)

    return base64_bytes.decode(ecoding)


def is_windows():

    return sys.platform in ["win32", "cygwin", "msys"]


def format_path_for(path: str, os: OS):

    if os in (OS.LINUX, OS.MAC):
        return path.replace("\\", "/")

    elif os == OS.WINDOWS:
        return path.replace("/", "\\")


def format_path_for_os(path: str):

    if sys.platform in ["win32", "cygwin", "msys"]:
        return format_path_for(path, OS.WINDOWS)

    elif sys.platform in ["linux", "linux2"]:
        return format_path_for(path, OS.LINUX)

    elif sys.platform in ["darwin"]:
        return format_path_for(path, OS.MAC)

    else:
        raise Exception(
            f"Error formating path={path} for os. Operating system not supported {sys.platform}"
        )
