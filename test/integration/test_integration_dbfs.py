
from autobricks import Dbfs
import pytest
import os

SKIP_INTEGRATION = os.getenv("SKIP_INTEGRATION")


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_dbfs_upload():

    to_root = "/temp"
    to_path_dir = f"{to_root}/upload_test/"
    to_file = "UploadTest.txt"
    to_path =  f"{to_path_dir}{to_file}"
    from_path = f'./test/artefacts/{to_file}'

    Dbfs.dbfs_upload(from_path, to_path, True)

    result = Dbfs.dbfs_get_status(to_path)
    expected = {'path': '/temp/upload_test/UploadTest.txt', 'is_dir': False, 'modification_time':result['modification_time'], 'file_size': result['file_size']}
    
    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_dbfs_list():

    to_root = "/temp"
    to_path_dir = f"{to_root}/upload_test/"

    result = Dbfs.dbfs_list(to_path_dir)
    expected = {'files': [{'path': '/temp/upload_test/UploadTest.txt', 'is_dir': False, 'modification_time':result['files'][0]['modification_time'], 'file_size': result['files'][0]['file_size']}]}

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_Dbfs_delete():

    host = os.environ["DATABRICKS_API_HOST"]
    to_root = "/temp"
    to_path_dir = f"{to_root}/upload_test/"
    to_file = "UploadTest.txt"
    to_path =  f"{to_path_dir}{to_file}"

    Dbfs.dbfs_delete_file(to_path_dir, True)

    expected = f"404 Client Error: Not Found for url: {host}/api/2.0/dbfs/get-status"
    
    try:
        result = Dbfs.dbfs_get_status(to_path)
    except Exception as e:
        result = str(e)

    assert result == expected

