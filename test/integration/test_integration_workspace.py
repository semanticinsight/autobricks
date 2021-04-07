from autobricks import Workspace
import json
from dataclasses import dataclass
import pytest
import os

SKIP_INTEGRATION = os.getenv("SKIP_INTEGRATION") == "True"

@dataclass
class Config:

    workspace_root: str
    project_folder: str
    test_notebook_root: str
    test_project: str
    win_test_notebook_root: str


@pytest.fixture
def test_config():

    workspace_root = "/__autobricks_test"
    project = "/project"
    test_notebook_root = "./test/artefacts/notebooks"
    test_project = f"{test_notebook_root}{project}"
    win_test_notebook_root =  ".\\test\\artefacts\\notebooks"

    return Config(
        workspace_root,
        project,
        test_notebook_root,
        test_project,
        win_test_notebook_root
    )


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_mkdirs(test_config):

    Workspace.workspace_mkdirs(test_config.workspace_root)
    result = Workspace.workspace_get_status(test_config.workspace_root)

    expected = {
        "object_type": "DIRECTORY", 
        "path": test_config.workspace_root, 
        "object_id": result["object_id"]
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_import_source(test_config):

    Workspace.workspace_import(
        f"{test_config.test_project}/notebook_source.py" , 
        f"{test_config.workspace_root}/notebook_source", 
        Workspace.Format.SOURCE,  
        Workspace.Language.PYTHON, 
        True)

    result = Workspace.workspace_get_status(f"{test_config.workspace_root}/notebook_source")

    expected = {
        "object_type": "NOTEBOOK", 
        "path": f"{test_config.workspace_root}/notebook_source", 
        "language": "PYTHON", 
        "object_id": result["object_id"]
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_import_html(test_config):

    Workspace.workspace_import(
        f"{test_config.test_project}/notebook_html.html", 
        f"{test_config.workspace_root}/notebook_html", 
        Workspace.Format.HTML,    
        Workspace.Language.PYTHON, 
        True)

    result = Workspace.workspace_get_status(f"{test_config.workspace_root}/notebook_html")

    expected = {
        "object_type": "NOTEBOOK", 
        "path": f"{test_config.workspace_root}/notebook_html", 
        "language": "PYTHON", 
        "object_id": result["object_id"]
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_import_jupyter(test_config):

    Workspace.workspace_import(
        f"{test_config.test_project}/notebook_jupyter.ipynb", 
        f"{test_config.workspace_root}/notebook_jupyter", 
        Workspace.Format.JUPYTER, 
        Workspace.Language.PYTHON, 
        True)

    result = Workspace.workspace_get_status(f"{test_config.workspace_root}/notebook_jupyter")

    expected = {
        "object_type": "NOTEBOOK", 
        "path": f"{test_config.workspace_root}/notebook_jupyter", 
        "language": "PYTHON", 
        "object_id": result["object_id"]
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_import_dbc(test_config):

    Workspace.workspace_import(
        f"{test_config.test_project}/notebook_dbc.dbc", 
        f"{test_config.workspace_root}/notebook_dbc",
        Workspace.Format.DBC,
        Workspace.Language.PYTHON,
        False)

    result = Workspace.workspace_get_status(f"{test_config.workspace_root}/notebook_dbc")

    expected = {
        "object_type": "NOTEBOOK", 
        "path": f"{test_config.workspace_root}/notebook_dbc", 
        "language": "PYTHON", 
        "object_id": result["object_id"]
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_list(test_config):

    result = Workspace.workspace_list(test_config.workspace_root)
    result["objects"][0]["object_id"]

    expected = {"objects": [
        {"object_type": "NOTEBOOK", "path": f"{test_config.workspace_root}/notebook_source", "language": "PYTHON", "object_id": result["objects"][0]["object_id"]}, 
        {"object_type": "NOTEBOOK", "path": f"{test_config.workspace_root}/notebook_html", "language": "PYTHON", "object_id": result["objects"][1]["object_id"]}, 
        {"object_type": "NOTEBOOK", "path": f"{test_config.workspace_root}/notebook_jupyter", "language": "PYTHON", "object_id": result["objects"][2]["object_id"]}, 
        {"object_type": "NOTEBOOK", "path": f"{test_config.workspace_root}/notebook_dbc", "language": "PYTHON", "object_id": result["objects"][3]["object_id"]}
    ]}
    
    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_export_source(test_config):

    result = Workspace.workspace_export(
        f"{test_config.workspace_root}/notebook_source", 
        Workspace.Format.SOURCE, 
        test_config.test_notebook_root)

    expected = {
        "from_path": f"{test_config.workspace_root}/notebook_source", 
        "to_path": f"{test_config.test_notebook_root}/notebook_source.py", 
        "file_type": "SOURCE"
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_export_html(test_config):

    result = Workspace.workspace_export(
        f"{test_config.workspace_root}/notebook_html", 
        Workspace.Format.HTML, 
        test_config.test_notebook_root)

    expected = {
        "from_path": f"{test_config.workspace_root}/notebook_html", 
        "to_path": f"{test_config.test_notebook_root}/notebook_html.html", 
        "file_type": "HTML"
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_export_jupyter(test_config):

    result = Workspace.workspace_export(
        f"{test_config.workspace_root}/notebook_jupyter", 
        Workspace.Format.JUPYTER, 
        test_config.test_notebook_root)

    expected = {
        "from_path": f"{test_config.workspace_root}/notebook_jupyter", 
        "to_path": f"{test_config.test_notebook_root}/notebook_jupyter.ipynb", 
        "file_type": "JUPYTER"
        }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_export_dbc(test_config):

    result = Workspace.workspace_export(
        f"{test_config.workspace_root}/notebook_dbc", 
        Workspace.Format.DBC, 
        test_config.test_notebook_root)

    expected = {
        "from_path": f"{test_config.workspace_root}/notebook_dbc", 
        "to_path": f"{test_config.test_notebook_root}/notebook_dbc.dbc", 
        "file_type": "DBC"
    }

    assert result == expected


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_delete(test_config):

    Workspace.workspace_delete(test_config.workspace_root, True)

    try:
        result = Workspace.workspace_get_status(test_config.workspace_root)
    except Exception as e:
        result = str(e)

    expected = "404 Client Error: Not Found for url"
    
    assert expected in result


@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_workspace_import_dir(test_config):

    if Workspace.workspace_dir_exists(test_config.workspace_root):
        Workspace.workspace_delete(test_config.workspace_root, True)
        
    result = Workspace.workspace_import_dir(
        test_config.win_test_notebook_root, 
        test_config.project_folder, 
        test_config.workspace_root, 
        Workspace.DeployMode.MOVE
    )

    result = Workspace.workspace_dir_exists(test_config.workspace_root)
    result = result and Workspace.workspace_dir_exists(f"{test_config.workspace_root}/level_1_1")
    result = result and Workspace.workspace_dir_exists(f"{test_config.workspace_root}/level_1_2")
    result = result and Workspace.workspace_dir_exists(f"{test_config.workspace_root}/level_1_1/level2")
    result = result and Workspace.workspace_notebook_exists(f"{test_config.workspace_root}/level_1_1/notebook_l1_1_source")
    result = result and Workspace.workspace_notebook_exists(f"{test_config.workspace_root}/level_1_2/notebook_l1_2_source")
    result = result and Workspace.workspace_notebook_exists(f"{test_config.workspace_root}/level_1_1/level2/notebook_l2_source")
    
    if Workspace.workspace_dir_exists(test_config.workspace_root):
        Workspace.workspace_delete(test_config.workspace_root, True)

    assert result

