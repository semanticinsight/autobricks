# Cluster

This module contains functions to working with databricks clusters.

## cluster_name_exists


```python
cluster_name_exists(name: str)-> bool
```

<br />

| Parameter | Description |
|-----------|-------------|
| `name`    | Name of the cluster. Note that more than one cluster with the same name can exist within a given databricks workspace since they are uniquely identified by the cluster_id and not their name. |

<br />

A predicate function that can be used to check if a cluster with a given name already exists.

## cluster_get_by_name

```python
cluster_get_by_name(name: str)-> list
```

<br />

| Parameter | Description |
|-----------|-------------|
| `name`    | Name of the cluster. Note that more than one cluster with the same name can exist within a given databricks workspace since they are uniquely identified by the cluster_id and not their name. |

<br />

Returns a list of cluster details that have a matching name. Note that more than one cluster with the same name can exist with a given databricks workspace since they are uniquely identified by the cluster_id and not their name. The function response therefore returns a list of cluster objects. [The response dictionary for a cluster object can be seen in the API documentation](https://docs.databricks.com/dev-tools/api/latest/clusters.html#get)

## cluster_action

```python
cluster_action(
    cluster_id: str, 
    cluster_action: ClusterAction
) -> dict
```

Executes a cluster action for given cluster using the `cluster_id`. The `ClusterAction` can be imported from the `cluster` module. The function is an asynchonous call and will not wait for the operation to complete. Note that a cluster must be unpinned before it can be deleted.

Note that there are higher level functions in this module for waiting for running and waiting for clusters states, please see:

- `clusters_create`
- `cluster_wait_until_state`

Cluster actions are fairly self explanatory. [Pinned clusters](cluster_wait_until_state) will remain in the workspace UI list. Unpinned clusters are deleted after 30 days.

```python
from cluster import ClusterAction

for a in ClusterAction:
    print(a)
```
```
>>> ClusterAction.PIN
>>> ClusterAction.UNPIN
>>> ClusterAction.START
>>> ClusterAction.RESTART
>>> ClusterAction.STOP
>>> ClusterAction.DELETE
```


## clusters_create

Creates clusters defined in YAML files in the `cluster_defn_folder`. The cluster definition structure follows the [json schema defined](https://docs.databricks.com/dev-tools/api/latest/clusters.html#request-structure-of-the-cluster-definition) for the API but is YAML for easier coding. See `cluster_create`.


```python
clusters_create(
    cluster_defn_folder: str,
    pin: bool = True,
    stop: bool = True,
    delete_if_exists: bool = False,
    allow_duplicate_names: bool = False,
    init_script_path: str = None,
)
```

<br />

| Parameter | Description |
|-----------|-------------|
| `cluster_defn_folder   `    | Path of yaml files that hold cluster definitions. YAML supports variable replacements see example below  |
| `pin`                       | Whether the cluster should be pinned in the UI  |
| `stop`                      | By default databricks will start a cluster that is created. Use this parameter to stop the cluster from starting on creation   |
| `delete_if_exists`          | If the cluster name already exists then unpin and delete the existing cluster |
| `allow_duplicate_names`     | Clusers are uniquely identified by an id, use this parameter if you wish to enforce unique names. Note that if this is `False`, the name already exists and `delete_if_exists` is `False` then the creation will fail.  |
| `init_script_path`          | Path to an init sh script that you may want to deploy with cluster. Ensure that the `init_script.dbfs[].destination` is defined.|

<br />

## cluster_create

Creates a cluster defined a YAML file in the `cluster_defn_path`. The cluster definition structure follows the [json schema defined](https://docs.databricks.com/dev-tools/api/latest/clusters.html#request-structure-of-the-cluster-definition) for the API but is YAML for easier coding. See `cluster_create`.

```python
cluster_create(
    cluster_defn_path: str,
    pin: bool = True,
    stop: bool = True,
    delete_if_exists: bool = False,
    allow_duplicate_names: bool = False,
    init_script_path: str = None,
) -> dict
```
<br />

| Parameter | Description |
|-----------|-------------|
| `cluster_defn_path   `      | Path of the yaml file that holds the definition. YAML supports variable replacements see example below  |
| `pin`                       | Whether the cluster should be pinned in the UI  |
| `stop`                      | By default databricks will start a cluster that is created. Use this parameter to stop the cluster from starting on creation   |
| `delete_if_exists`          | If the cluster name already exists then unpin and delete the existing cluster |
| `allow_duplicate_names`     | Clusers are uniquely identified by an id, use this parameter if you wish to enforce unique names. Note that if this is `False`, the name already exists and `delete_if_exists` is `False` then the creation will fail.  |
| `init_script_path`          | Path to an init sh script that you may want to deploy with cluster. Ensure that the `init_script.dbfs[].destination` is defined.|

<br />
The cluster definition supports variable injection to help conventional naming. For example a file store at `{cluster_defn_path}/my_cluster.yaml` will create a cluster called `my_cluster_7.5` with logs and init scripts stored under a leaf folder with that name. Variables are:


| Variable | Description |
|-----------|-------------|
| `{filename}`     | The filename of the cluster definition. Handy to drive the name of the cluster using the definition file name  |
| `{dbr}`              | The major and minor value of the DBR runtime  |
| `{cluster_name}`     | The name of the cluster, used in the exmaple below to create the logs and reference the init script   |


For example:


```yaml
num_workers: 1
cluster_name: "{filename}_{dbr}"
spark_version: "7.5.x-cpu-ml-scala2.12"
spark_conf":
  spark.databricks.cluster.profile: "serverless"
  spark.databricks.passthrough.enabled: "true"
  spark.databricks.pyspark.enableProcessIsolation: "true"
  spark.databricks.repl.allowedLanguages: "python,sql"
azure_attributes:
  first_on_demand: 1
  availability: ON_DEMAND_AZURE
  spot_bid_max_price: -1
node_type_id: "Standard_DS3_v2"
driver_node_type_id: "Standard_DS3_v2"
ssh_public_keys:
custom_tags:
  deployed_by: "AzureDevOps"
 cluster_log_conf:
   dbfs:
     destination: "dbfs:/FileStore/cluster/logs/{cluster_name}"
 init_scripts:
   - dbfs:
       destination: "dbfs:/FileStore/cluster/init/{cluster_name}.sh"
spark_env_vars:
  ENVIRONMENT: "TEST"
autotermination_minutes: 30
enable_elastic_disk: true
```

## cluster_delete_clusters:

```python
cluster_delete_clusters(clusters: list)
```

Deletes the clusters in the list. The list would be list of cluster objects. In order for the function to delete a cluster each object must have a `cluster_id` attribute; other attributes maybe present. For example the following would be valid

```json
[{"cluster_id":"1"}, {"cluster_id":"2"}, {"cluster_id":"3"}]
```

## cluster_list

```python
cluster_list() -> dict
```

Returns a list of cluster [cluster definitions](https://docs.databricks.com/dev-tools/api/latest/clusters.html#request-structure-of-the-cluster-definition).


## get_cluster_state

```python
get_cluster_state(cluster_id: str) -> ClusterState
```

Gets the clusters state for a given `cluster_id`. Note the self explanatory `ClusterState` enum:

```
ClusterState.PENDING
ClusterState.RUNNING
ClusterState.RESTARTING
ClusterState.RESIZING
ClusterState.TERMINATING
ClusterState.TERMINATED
ClusterState.ERROR
ClusterState.UNKNOWN
```


## cluster_is_running

```python
cluster_is_running(cluster_id: str) -> bool
```
Returns `True` if a cluster with the cluster_id is in the `ClusterState.RUNNING` state

## cluster_is_terminated

```python
cluster_is_terminated(cluster_id: str) -> bool
```

Returns `True` if a cluster with the cluster_id is in the `ClusterState.TERMINATING` state

## cluster_get


```python
cluster_get(cluster_id: str) -> dict
```
Gets a [cluster definition](https://docs.databricks.com/dev-tools/api/latest/clusters.html#request-structure-of-the-cluster-definition) for a given `cluster_id`

## cluster_wait_until_state

```python
cluster_wait_until_state(
    cluster_id: str, 
    cluster_state: ClusterState, 
    wait_seconds: int = 10
)
```

This is a blocking call that will wait for a given `ClusterState` to be reached for a given `cluster_id`. `wait_seconds` is the interval the blocking call will wait between calls that check if the state has been reached. WARNING: setting `wait_seconds` too low may cause the API limits to be exceeded.

Note the self explanatory `ClusterState` enum:

```
ClusterState.PENDING
ClusterState.RUNNING
ClusterState.RESTARTING
ClusterState.RESIZING
ClusterState.TERMINATING
ClusterState.TERMINATED
ClusterState.ERROR
ClusterState.UNKNOWN
```

## cluster_has_tag

```python
cluster_has_tag(
    cluster: dict, 
    tag_key: str, 
    tag_value: str
) -> bool
```

Returns `True` if a given cluster definition with a `cluster_id` has a `tag_key` with the value `tag_value`

## clusters_clear_down

```python
clusters_clear_down(
    tag_key: str = None, 
    tag_value: str = None, 
    show_only: bool = True
)
```

Deletes all clusters optionally with a certain `tag_key` and `tag_value`. `show_only` = `True` allows the caller to output the clusters to check what will be deleted. Setting `show_only` = `False` will execute the deletion.


## cluster_log_states

```python
cluster_log_states()
```


## cluster_run

```python
cluster_run(cluster_id: str)
```

Runs a cluster with a given `cluster_id` and waits for to the reach the running state or to terminate with error. This call will handle the repsonse if the cluster has already been started but isn't running yet. If the cluster has already started when this is called it will return when either the cluster has reach a running state or terminated with error.

