import requests
import requests_mock
import sys
import base64
from pytest_mock import mocker
from autobricks import Configuration
from autobricks import Dbfs, ApiUtils
from dataclasses import dataclass
import pytest
from unittest.mock import patch, mock_open
from unittest import mock


@pytest.fixture
def config():
    @dataclass
    class Config:
        config: dict
        host: str
        version: str
        endpoint: str

    return Config(
        config=Configuration.config,
        host = Configuration.config["databricks_api_host"],
        version="2.0", 
        endpoint="dbfs"
    )


@pytest.fixture
def api_service():

    api_service = ApiUtils.ApiService(config.config)
    return api_service


@pytest.fixture
def api_utils_mock(mocker, config, api_service):

    mocker.patch.object(ApiUtils, "API_VERSION", config.version)
    mocker.patch.object(Dbfs, "_api_service", api_service)


def test_dbfs_list(requests_mock, config):

    expected = {
        "files": [
            {
                "file_size": 0,
                "is_dir": True,
                "modification_time": 1613340990000,
                "path": "/FileStore",
            },
            {
                "file_size": 128,
                "is_dir": False,
                "modification_time": 1612027998000,
                "path": "/test.txt",
            },
        ]
    }

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/list", json=expected
    )

    result = Dbfs.dbfs_list("/")

    assert expected == result


def test_dbfs_get_status(requests_mock, config):

    expected = {
        "path": "/path/of/file",
        "is_dir": False,
        "file_size": 10,
        "modification_time": 0,
    }

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/get-status",
        json=expected,
    )

    result = Dbfs.dbfs_get_status(expected["path"])

    assert expected == result


def test_dbfs_delete(requests_mock, config):

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/delete", json={}
    )

    result = Dbfs.dbfs_delete_file("/path/of/file", True)

    assert {} == result


def test_dbfs_mkdirs(requests_mock, config):

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/mkdirs", json={}
    )

    result = Dbfs.dbfs_mkdirs("/path/of/file")

    assert {} == result


def test_dbfs_move(requests_mock, config):

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/move", json={}
    )

    result = Dbfs.dbfs_move("/path/from/here", "/path/to/here")

    assert {} == result


def test_dbfs_read(requests_mock, config):

    path = "/path/of/file"
    offset = 1024
    length = 1024

    expected = {"bytes_read": length, "data": "b10101010110"}

    requests_mock.get(
        f"{config.host}/api/{config.version}/{config.endpoint}/read", json=expected
    )

    result = Dbfs.dbfs_read(path, offset, length)

    assert expected == result


def test_dbfs_download_large(requests_mock, config):

    from_path = "/path/of/file"
    to_path = "./text.txt"
    length = 1024
    data = "SGVsbG8gV29ybGQ="
    url = f"{config.host}/api/{config.version}/{config.endpoint}/read"

    expected = [
        {"bytes_read": length, "data": data}, 
        {"bytes_read": 4,      "data": data}
    ]

    content = data.encode("utf-8")
    content = base64.b64decode(content)

    for e in expected:
        requests_mock.get(url, json=e)

    with patch("builtins.open", mock_open()) as mocked_file:

        Dbfs.dbfs_download(from_path, to_path)

        mocked_file.assert_called_once_with(to_path, "wb")

        handle = mocked_file()
        handle.write.assert_has_calls(
            [
                mock.call(content)
            ]
        )


def test_dbfs_download(requests_mock, config):

    from_path = "/path/of/file"
    to_path = "./text.txt"
    length = 1024
    data = "SGVsbG8gV29ybGQ="
    url = f"{config.host}/api/{config.version}/{config.endpoint}/read"

    expected = [
        {"bytes_read": length, "data": data}, 
        {"bytes_read": 4,      "data": data}
    ]

    content = data.encode("utf-8")
    content = base64.b64decode(content)

    with patch("builtins.open", mock_open()) as mocked_file:

        for e in expected:
            requests_mock.get(url, json=e)
        Dbfs.dbfs_download(from_path, to_path)

        mocked_file.assert_called_once_with(to_path, "wb")

        # assert if write(content) was called from the file opened
        # in another words, assert if the specific content was written in file
        handle = mocked_file()
        handle.write.assert_called_once_with(content)


def test_dbfs_find_file():

    result = Dbfs.find_file("test*dbfs.py", "./test/unit")

    assert result == ["./test/unit/test_dbfs.py"]


def test_read_file_block():

    path = "/path/of/file.txt"
    length = 1024
    data = "booyakashaan!"

    content = data.encode("utf-8")
    content = base64.b64decode(content)

    read_data = ""
    with patch("builtins.open", mock_open(read_data=data)) as mocked_file:

        with open(path, "rb") as f:
            for block in Dbfs._read_file_block(f, 1):
                read_data = read_data + str(block)

    assert read_data == data


def test_dbfs_upload(requests_mock, config):

    data = "booyakashaan!"
    path = "/path/of/file.txt"
    datarb = b"booyakashaan!"

    content = data.encode("utf-8")
    content = base64.b64decode(content)

    create_expected = {"handle": 1}
    expected = {}

    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/create",
        json=create_expected,
    )
    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/add-block", json={}
    )
    requests_mock.post(
        f"{config.host}/api/{config.version}/{config.endpoint}/close", json={}
    )

    with patch("builtins.open", mock_open(read_data=datarb)) as mocked_file:

        result = Dbfs.dbfs_upload(path, path, True)
        mocked_file.assert_called_once_with(path, "rb")

        handle = mocked_file()
        handle.read.assert_called_with(1024)
        handle.read.assert_called_with(1024)

    assert result == expected
