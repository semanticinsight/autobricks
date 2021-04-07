# Job


This module contains functions to working with databricks Jobs.


## [job_run_get](https://docs.databricks.com/dev-tools/api/latest/jobs.html#get)

Retrieve information about a single job. 

```python
job_run_get(run_id: int)-> dict()
```


[See return dictionary](https://docs.databricks.com/dev-tools/api/latest/jobs.html#get)


## [job_runs_list](https://docs.databricks.com/dev-tools/api/latest/jobs.html#list)

Returns an array of job runs

```python
job_runs_list()->list
```

[See return dictionary](https://docs.databricks.com/dev-tools/api/latest/jobs.html#list)


## [job_run_delete](https://docs.databricks.com/dev-tools/api/latest/jobs.html#delete)

Delete a job and send an email to the addresses specified in JobSettings.email_notifications. No action occurs if the job has already been removed. After the job is removed, neither its details nor its run history is visible in the Jobs UI or API. The job is guaranteed to be removed upon completion of this request. However, runs that were active before the receipt of this request may still be active. They will be terminated asynchronously.

```python
job_run_delete(run_id: int)
```

[See return dictionary](https://docs.databricks.com/dev-tools/api/latest/jobs.html#delete)

## [job_run_submit](https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-submit)

Submit a one-time run. This endpoint allows you to submit a workload directly without creating a job. Runs submitted using this endpoint don’t display in the UI. Use the jobs/runs/get API to check the run state after the job is submitted.

```python
job_run_submit(
    notebook_path: str,
    run_name: str = "default",
    spark_version: str = "7.3.x-scala2.12",
    node_type_id: str = "Standard_DS3_v2",
    driver_node_type_id: str = "Standard_DS3_v2",
    num_workers: int = 1,
    timeout_seconds: int = 900,
    idempotency_token: UUID = None,
    cluster_id: str = None,
)
```

Provide minimal details for an on demand job cluster or provide a `cluster_id` for a specific named cluster already in the workspace.

[see details here](https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-submit).


## job_run_notebook

Run  a notebook against a specific `cluster_id` and wait for it for to finish in error or success. `wait_seconds` is the interval time between calls that check the status of the job sto see if it's finished. WARNING: setting `wait_seconds` too low could exceed the API call limits.

```python
job_run_notebook(
    notebook_path: str,
    name: str = "default",
    idempotency_token: UUID = None,
    cluster_id: str = None,
    wait_seconds: int = 5,
)
```