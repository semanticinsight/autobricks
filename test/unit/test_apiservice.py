
from autobricks.api_service import (
    ApiService, 
    configuration, 
    AutobricksConfigurationInvalid
)
from autobricks.api_service._auth_factory import AuthenticationType
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
        config=configuration,
        host = configuration["databricks_api_host"],
        version="2.0",
        function="testfunc",
        endpoint="endpoint",
        data={"data": "data"},
        query="item=1",
    )


@pytest.fixture
def api_utils_mock(mocker, config):

    mocker.patch.object(api_service, "API_VERSION", config.version)


@pytest.fixture
def api_service(config):

    api_svc = ApiService(config.config)
    return api_svc


def test_get_data_query(requests_mock, config, api_service):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}?{config.query}",
        json=config.data,
    )
    
    response = api_service.api_get(
        config.endpoint, config.function, config.data, config.query
    )

    assert config.data == response


def test_get_data_query_exception(requests_mock, config, api_service):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}?{config.query}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = api_service.api_get(
            config.endpoint, config.function, config.data, config.query
        )
    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_get_data(requests_mock, config, api_service):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = api_service.api_get(config.endpoint, config.function, config.data)

    assert config.data == response


def test_get_data_query_exception(requests_mock, config, api_service):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = api_service.api_get(config.endpoint, config.function, config.data)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_get(requests_mock, config, api_service):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = api_service.api_get(config.endpoint, config.function)

    assert config.data == response


def test_get_exception(requests_mock, config, api_service):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = api_service.api_get(config.endpoint, config.function)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_post_data(requests_mock, config, api_service):

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = api_service.api_post(config.endpoint, config.function, config.data)

    assert config.data == response


def test_post_data_exception(requests_mock, config, api_service):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.post(url, text=error_text, status_code=error_code)
    
    result = None
    try:
        response = api_service.api_post(config.endpoint, config.function, config.data)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result

def test_api_service_auth_type_exception(config):
    """So that ApiService configuration is usable
        Given a configuration that contains no auth type
        Then a meaningfull exception should be thrown
    """
    var = "auth_type"
    tconfig = dict(config.config)
    del tconfig[var]

    values = ", ".join([v.name for v in AuthenticationType])
    msg = f"Autobricks configuration variable '{var}' is not valid. {var}=None. Valid values are: {values}"
    with pytest.raises(AutobricksConfigurationInvalid, match=msg):
        api_svc = ApiService(config=tconfig)

def test_api_service_api_host_exception(config):
    """So that ApiService configuration is usable
        Given a configuration that contains no databricks_api_host
        Then a meaningfull exception should be thrown
    """
    var = "databricks_api_host"
    tconfig = dict(config.config)
    del tconfig[var]

    msg = f"Autobricks configuration variable '{var}' is not valid. {var}=None"
    with pytest.raises(AutobricksConfigurationInvalid, match=msg):
        api_svc = ApiService(config=tconfig)
