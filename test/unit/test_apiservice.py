from autobricks import ApiService
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


@pytest.fixture
def api_utils_mock(mocker, config):

    mocker.patch.object(ApiService, "API_VERSION", config.version)


@pytest.fixture
def api_service(config):

    api_service = ApiService.ApiService(config.config)
    return api_service


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


