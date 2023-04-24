from .api_service import ApiService, autobricks_logging
from enum import Enum
from typing import Union

_logger = autobricks_logging.get_logger(__name__)

endpoint = "jobs"
_JOBS_API_VERSION = "2.1"
_api_service = ApiService()

class JobRunException(Exception):
    def __init__(self, run_id: int):
        self.message = f"Failed on run_id={run_id}"
        super().__init__(self.message)

class JobException(Exception):
    def __init__(self, name: Union[str,int]):
        if isinstance(name, int):
            msg = f"Failed on job job_id={name}"
        else:
            msg = f"Failed on job name={name}"

        self.message = msg
        super().__init__(self.message)

class JobRunType(Enum):

    JOB_RUN = "JOB_RUN"
    WORKFLOW_RUN = "WORKFLOW_RUN"
    SUBMIT_RUN = "SUBMIT_RUN"

def job_run_get(run_id: int):

    params = {"run_id": run_id}
    try:
        response = _api_service.api_get(
            endpoint, "runs/get", params=params, api_version=_JOBS_API_VERSION
    )
    except Exception:
        raise JobRunException(run_id)

    return response


def job_runs_list(
        active_only:bool=False,
        completed_only:bool=False,
        job_id:int = None,
        offset:int = 0,
        limit:int = 25,
        run_type:JobRunType=JobRunType.JOB_RUN,
        expand_tasks=False,
        start_time_from:int=None,
        start_time_to:int=None
):
    
    params = {
        "active_only": active_only,
        "completed_only": completed_only,
        "job_id": job_id,
        "offset": offset,
        "limit": limit,
        "run_type": run_type.value,
        "expand_tasks": expand_tasks,
        "start_time_from": start_time_from,
        "start_time_to":start_time_to
    }
    params = {k:v for k, v in params.items() if v is not None}

    response = _api_service.api_get(
        endpoint, "runs/list", 
        api_version=_JOBS_API_VERSION
    )
    
    return response


def job_run_delete(run_id: int):
    data = {"run_id": run_id}
    try:
        response = _api_service.api_post(endpoint, "runs/delete", data, api_version=_JOBS_API_VERSION)
    except Exception:
        response = {}

    return response


def job_create(job:dict):

    name = job.get("name", "Unknown")
    try:
        response = _api_service.api_post(endpoint, "create", job, api_version=_JOBS_API_VERSION)
    except Exception:
        raise JobException(name)

    return response


def job_delete(job_id: int):

    data = {"job_id": job_id}
    try:
        response = _api_service.api_post(endpoint, "delete", data, api_version=_JOBS_API_VERSION)
    except Exception:
        raise JobException(job_id)

    return response


def job_update(job:dict):

    name = job.get("name", "Unknown")
    try:
        response = _api_service.api_post(endpoint, "update", job, api_version=_JOBS_API_VERSION)
    except Exception:
        raise JobException(name)

    return response


def job_get_by_id(job_id: int):

    params = {"job_id": job_id}

    try:
        response = _api_service.api_get(
            endpoint, "get", 
            api_version=_JOBS_API_VERSION,
            params=params
        )
    except Exception:
        raise JobException(job_id)
    
    return response


def job_get_by_name(name:str, expand_tasks:bool=False):

    params = {"name": name, "expand_tasks":expand_tasks}
    try:
        response = _api_service.api_get(
            endpoint, "list", 
            api_version=_JOBS_API_VERSION,
            params=params
        )
    except Exception:
        raise JobException(name)
    
    return response.get("jobs")


def job_get_id(name:str):

    jobs = job_get_by_name(name)
    if jobs:
        job_id = jobs[0].get("job_id", False)
        return job_id
    else:
        return None
    
def job_recreate(job:dict):

    name = job.get("name", "Unknown")

    job_id = job_get_id(name)
    if job_id:
        job_delete(job_id=job_id)

    job_create(job=job)