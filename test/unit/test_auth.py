import sys
from pytest_mock import mocker
from unittest.mock import Mock
from autobricks.Auth import (
    UserAuth,
    SPAuth,
    SPMgmtEndpointAuth
)
from autobricks import Configuration
from dataclasses import dataclass
import pytest


@pytest.fixture
def config():
    @dataclass
    class Config:
        config: dict
        host: str
        version: str
        function: str
        endpoint: str
        data: dict
        query: str

    return Config(
        config=Configuration.config,
        host = Configuration.config["databricks_api_host"],
        version="2.0",
        function="testfunc",
        endpoint="endpoint",
        data={"data": "data"},
        query="item=1",
    )


# @pytest.fixture
# def api_utils_mock(mocker, config):

#     mocker.patch.object(ApiUtils, "API_VERSION", config.version)


# @pytest.fixture
# def api_service(config):

#     api_service = ApiUtils.ApiService(config.config)
#     return api_service


def test_user_auth_header(config):
    """When: the authorisation type is user
       Then: the UserAuth.get_headers() should return
             a bearer token header holding the dbutilstoken 
    """

    token = config.config.get("dbutilstoken")
    expected = {"Authorization": f"Bearer {token}"}
    auth = UserAuth(config.config)
    result = auth.get_headers()

    assert expected == result


def test_user_auth_header_keyerror(config):
    """When: the authorisation type is user 
             and the configuration is missing 
             the dbutilstoken

       Then: the UserAuth.get_headers() should return
             a informative expception 
    """
    
    del config.config["dbutilstoken"]
    a = Mock()
    a.side_effect = ValueError("dbutilstoken key not found in UserAuth parameters")
    with pytest.raises(ValueError, match="dbutilstoken key not found in UserAuth parameters"):
        auth = UserAuth(config.config)
