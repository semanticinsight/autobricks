import requests
import requests_mock
import sys
from pytest_mock import mocker
from autobricks import ApiUtils
from dataclasses import dataclass
import pytest
import os


@pytest.fixture
def config():
    @dataclass
    class Config:
        host: str
        token: str
        version: str
        function: str
        endpoint: str
        data: dict
        query: str

    return Config(
        host="https://wwww.autobricks.net",
        token="dapixxx",
        version="2.0",
        function="testfunc",
        endpoint="endpoint",
        data={"data": "data"},
        query="item=1",
    )


@pytest.fixture
def api_utils_mock(mocker, config):

    mocker.patch.object(ApiUtils, "host", config.host)
    mocker.patch.object(ApiUtils, "token", config.token)
    mocker.patch.object(ApiUtils, "API_VERSION", config.version)


def test_get_data_query(mocker, requests_mock, config, api_utils_mock):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}?{config.query}",
        json=config.data,
    )

    response = ApiUtils.api_get(
        config.endpoint, config.function, config.data, config.query
    )

    assert config.data == response


def test_get_data_query_exception(mocker, requests_mock, config, api_utils_mock):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}?{config.query}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = ApiUtils.api_get(
            config.endpoint, config.function, config.data, config.query
        )
    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_get_data(mocker, requests_mock, config, api_utils_mock):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = ApiUtils.api_get(config.endpoint, config.function, config.data)

    assert config.data == response


def test_get_data_query_exception(mocker, requests_mock, config, api_utils_mock):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = ApiUtils.api_get(config.endpoint, config.function, config.data)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_get(mocker, requests_mock, config, api_utils_mock):

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = ApiUtils.api_get(config.endpoint, config.function)

    assert config.data == response


def test_get_exception(mocker, requests_mock, config, api_utils_mock):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.get(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = ApiUtils.api_get(config.endpoint, config.function)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_post_data(requests_mock, config, api_utils_mock):

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}",
        json=config.data,
    )

    response = ApiUtils.api_post(config.endpoint, config.function, config.data)

    assert config.data == response


def test_post_data_exception(requests_mock, config, api_utils_mock):

    url = f"{config.host}/api/{config.version}/{config.endpoint}/{config.function}"
    error_text = "an error occurred"
    error_code = 404
    requests_mock.post(url, text=error_text, status_code=error_code)

    result = None
    try:
        response = ApiUtils.api_post(config.endpoint, config.function, config.data)

    except Exception as e:
        response = e.response

    result = response.text == error_text
    result = result and response.status_code == error_code

    assert result


def test_base64_decode_utf8():

    result = ApiUtils.base64_decode("SGVsbG8gV29ybGQ=").decode("utf-8")

    assert result == "Hello World"


def test_base64_encode_utf8():

    result = ApiUtils.base64_encode("Hello World".encode("utf-8"))

    assert result == "SGVsbG8gV29ybGQ="


def test_base64_decode_ascii():

    encoding = "ascii"
    result = ApiUtils.base64_decode("SGVsbG8gV29ybGQ=", encoding).decode(encoding)

    assert result == "Hello World"


def test_base64_encode_ascii():

    encoding = "ascii"
    result = ApiUtils.base64_encode("Hello World".encode(encoding), encoding)

    assert result == "SGVsbG8gV29ybGQ="


def test_post_data():

    mocker.patch.object(sys, "platform", "linux")

    assert not ApiUtils.is_windows()


def test_post_data(mocker):

    mocker.patch.object(sys, "platform", "win32")

    assert ApiUtils.is_windows()


def test_format_linux_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for_os("/not/a/windows/path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_part_linux_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for_os("/not/a\\windows/path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for_os("\\not\\a\\windows\\path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for_os("\\not\\a\\linux\\path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_part_win32_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for_os("\\not\\a/linux\\path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_linux_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for_os("/not/a/linux/path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_win32_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for_os("\\not\\a\\darwin\\path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_part_win32_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for_os("\\not\\a/darwin\\path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_darwin_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for_os("/not/a/darwin/path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_linux_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for("/not/a/windows/path", ApiUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_part_linux_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for("/not/a\\windows/path", ApiUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = ApiUtils.format_path_for("\\not\\a\\windows\\path", ApiUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for("\\not\\a\\linux\\path", ApiUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_part_win32_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for("\\not\\a/linux\\path", ApiUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_linux_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = ApiUtils.format_path_for("/not/a/linux/path", ApiUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_win32_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for("\\not\\a\\darwin\\path", ApiUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_part_win32_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for("\\not\\a/darwin\\path", ApiUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_linux_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = ApiUtils.format_path_for("/not/a/darwin/path", ApiUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_exception(mocker):

    path = "/not/a/darwin/path"
    osystem = "superduperos"
    mocker.patch.object(sys, "platform", osystem)

    expected = (
        f"Error formating path={path} for os. Operating system not supported {osystem}"
    )

    error_message = None
    try:
        result = ApiUtils.format_path_for_os(path)

    except Exception as e:
        error_message = str(e)

    assert error_message == expected


def test_is_windows(mocker):

    mocker.patch.object(sys, "platform", "win32")
    assert ApiUtils.is_windows()


def test_is_not_windows(mocker):

    mocker.patch.object(sys, "platform", "linux")
    assert not ApiUtils.is_windows()
