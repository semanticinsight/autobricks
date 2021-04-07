# Examples

The purpose of the library is to provide high level ptyhon scripting of deployment tasks using the databricks API.0

## Deploy Notebook, Run & Delete

```
from autobricks import Workspace, Job
from uuid import uuid4
from pprint import pprint

# deploy a notebook
Workspace.workspace_mkdirs("/__autobricks_test")
repsonse = Workspace.workspace_import("./integration_tests/notebook_run/submit_now.py" , "/__autobricks_test/submit_now", Workspace.Format.SOURCE,  Workspace.Language.PYTHON, True)
pprint(repsonse)

# run notebook using a job cluster
token = uuid4()
repsonse = Job.job_run_notebook("/__autobricks_test/submit_now", "autobricks_test_submit_now", token)
pprint(repsonse)

# clean up notebook
Workspace.workspace_delete("/__autobricks_test", True)
```

## Deploy Directory of Notebooks, Check Exists & Delete


This takes everything in `./integration_tests/notebooks/__autobricks_test` and deploys it to a databricks workspace directory `/__autobricks_test`

```python
# deploy directory of notebooks to workspace
result = Workspace.workspace_import_dir("./integration_tests/notebooks", "/__autobricks_test")

# to deploy a specific source directory
#result = Workspace.workspace_import_dir("./integration_tests/notebooks", "/__autobricks_test/my_sub_dir")

# check if the root folder exists
result = Workspace.workspace_dir_exists("/__autobricks_test")

# clean up the root folder
Workspace.workspace_delete("/__autobricks_test", True)
```



## Create a Cluster, Run It, Stop It and Delete

This example takes a cluster defined in a yaml file and deploys it to a workspace. Variables can be used in the yaml file to populate the name, for example:
```python
cluster_name: "{filename}_{dbr}"
```

- filename is the name of the yaml definition file
- dbr is the databricks runtime version



The following code creates a cluster using a definition yaml file. Starts the cluster and waits for it to reach a running state. Then it stops the cluster, waits for it to terminate, unpins it and deletes it.

```python
cluster_defn_file = "./integration_tests/clusters/autobricks_unittest.yaml"
response = cluster_create(cluster_defn_file, "1", delete_if_exists=False, stop=False)

# there can be more than 1 cluster with the same name
# the creation in this case forces there to be only 1 since allow_duplicate_names is False
cluster_id = response["clusters"][0]["cluster_id"]

# Run the cluster and wait for it to come up.
Cluster.cluster_run(cluster_id)

cluster_action(cluster_id, ClusterAction.STOP)
cluster_wait_until_state(cluster_id, ClusterState.TERMINATED)

cluster_action(cluster_id, ClusterAction.UNPIN)
cluster_action(cluster_id, ClusterAction.DELETE)
```

## Stop & Delete All Clusters with a Custom Tag

Stops and deletes all the clusters with the tag `deployed_by=devops`

```python
# clear down all the clusters with this tag
Cluster.clusters_clear_down("deployed_by", "devops")
```