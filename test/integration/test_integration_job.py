from autobricks import Workspace, Job
import json
from uuid import uuid4
from dataclasses import dataclass
import pytest
import os

SKIP_INTEGRATION = os.getenv("SKIP_INTEGRATION") == "True"

@dataclass
class Config:

    workspace_root: str
    artefacts_path: str


@pytest.fixture
def test_config():

    workspace_root = "/__autobricks_test"
    artefacts_path = "./test/artefacts"

    return Config(
        workspace_root,
        artefacts_path
    )

@pytest.mark.skipif(SKIP_INTEGRATION, reason="integration tests disabled")
def test_job_run_notebook(test_config):

    token = uuid4()
    Workspace.workspace_mkdirs(test_config.workspace_root)
    Workspace.workspace_import(
        f"{test_config.artefacts_path}/notebook_run/submit_now.py" , 
        f"{test_config.workspace_root}/submit_now.py", 
        Workspace.Format.SOURCE,  
        Workspace.Language.PYTHON, 
        True
    )

    result = Job.job_run_notebook(
        f"{test_config.workspace_root}/submit_now", 
        "autobricks_test_submit_now", 
        token
    )

    result = {
        'life_cycle_state': result['life_cycle_state'], 
        'result_state': result['result_state'], 
        'state_message': result['state_message'],
        'idempotency_token': result['idempotency_token']
    }

    expected = {
        'life_cycle_state': 'TERMINATED', 
        'result_state': 'SUCCESS', 
        'state_message': '',
        'idempotency_token': str(token)
    }

    Workspace.workspace_delete(test_config.workspace_root, True)

    assert result == expected

