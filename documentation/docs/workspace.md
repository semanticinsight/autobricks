# Workspace

This module contains functions to working with databricks Workspaces and deploying notebooks.

## workspace_import_dir

High level function for recursively depploying folders of notebooks to workspace. See the examples.


```python
workspace_import_dir(
    from_notebook_root: str,
    source_dir: str = "/",
    target_dir: str = None,
    deploy_mode: DeployMode = DeployMode.DEFAULT,
) -> list
```

- `from_notebook_root` - the root path of the notebook folder that you wish to deploy. e.g. to deploy `./build/notebooks` then the this path is `./build`
- `source_dir` - the directory to deploy. e.g. to deploy `notebooks` from `./build/notebooks/mystuff` then this path is `/notebooks`
- `target` - if not specified then folders are deployed as is to the root of the workspace. If provided then they it used as specified in the deployment mode.
- `deploy_mode` - The deployment modes work as follows:

| DeployMode	          | Description |
|-------------------------|-------------|
| `DeployMode.DEFAULT`    | `target_dir` isn't required. Deploys the content as is from the `source_dir` into the root of the workspace |
| `DeployMode.MOVE`	      | Deploys content contained within the `source_dir` into the `target_dir` in the workspace |
| `DeployMode.PARENT`	  | Deploys the `source_dir` under the `target_dir` in the root of the workspace |
| `DeployMode.CHILD`	  | Deploys the content of the `source_dir` into the workspace under the `source_dir` directory path and the target_dir child directory path |
| `DeployMode.ROOT_CHILD` | Deploys the content in the `source_dir` path into a directory path matching the `source_dir` path but with the target_dir directory injected following the root dir of the `source_dir` path |


## get_format

Covnerts a notebook extension into a format.

```python
get_format(extension: Extension) -> Format
```

Extension is defined as follows:

```python
class Extension(Enum):
    py = 1
    html = 2
    ipynb = 3
    dbc = 4
```

The returned format is defined as follows:

```python
class Format(Enum):
    SOURCE = 1
    HTML = 2
    JUPYTER = 3
    DBC = 4
```


## [workspace_import](https://docs.databricks.com/dev-tools/api/latest/workspace.html#import)

Import a notebook or the contents of an entire directory. If path already exists and overwrite is set to false, this call returns an error RESOURCE_ALREADY_EXISTS. You can use only DBC format to import a directory. Maps directly to the [API call](https://docs.databricks.com/dev-tools/api/latest/workspace.html#import) where the return details are specified.

```python
workspace_import(
    form_path: str, 
    to_path: str, 
    format: Format, 
    language: Language, 
    overwrite: True
)-> dict
```

- `form_path` - the local file path
- `to_path` - databricks workspace destination path
- `format` - Is the format of the notebook

```python
class Format(Enum):
    SOURCE = 1
    HTML = 2
    JUPYTER = 3
    DBC = 4 # note that DBC CANNOT BE OVER WRITTEN
```
- `language` - Is the lanaguage of the notebook

```python
class Language(Enum):
    SCALA = 1
    PYTHON = 2
    SQL = 3
    R = 4
```

- `overwrite` - whether or not to overwrite if the destination notebook already exists. Note that `Format.DBC` cannot be overwritten.

## [workspace_delete](https://docs.databricks.com/dev-tools/api/latest/workspace.html#delete)

Delete an object or a directory (and optionally recursively deletes all objects in the directory `path`). If `path` does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST. If path is a non-empty directory and `recursive` is set to false, this call returns an error DIRECTORY_NOT_EMPTY. Object deletion cannot be undone and deleting a directory recursively is not atomic. 

```python
workspace_delete(
    path: str, 
    recursive: True
) -> dict
```


## [workspace_get_status](https://docs.databricks.com/dev-tools/api/latest/workspace.html#get-status)

Gets the status of an object or a directory. If path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST. See the [API documentation](https://docs.databricks.com/dev-tools/api/latest/workspace.html#get-status) for return specification 

```python
workspace_get_status(path: str) -> dict
```

## [workspace_list](https://docs.databricks.com/dev-tools/api/latest/workspace.html#list)

List the contents of a directory, or the object if it is not a directory. If the input path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST. See the [API documentation](https://docs.databricks.com/dev-tools/api/latest/workspace.html#list) for return specification 

```python
workspace_list(path: str) -> list
```

## [workspace_mkdirs](https://docs.databricks.com/dev-tools/api/latest/workspace.html#mkdirs)

Create the given directory and necessary parent directories if they do not exists. If there exists an object (not a directory) at any prefix of the input path, this call returns an error RESOURCE_ALREADY_EXISTS. If this operation fails it may have succeeded in creating some of the necessary parent directories.

```python
workspace_mkdirs(path: str) -> dict
```

## [workspace_export](https://docs.databricks.com/dev-tools/api/latest/workspace.html#export)

Export a notebook or contents of an entire directory. If path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST. You can export a directory only in DBC format. If the exported data exceeds the size limit, this call returns an error MAX_NOTEBOOK_SIZE_EXCEEDED. This API does not support exporting a library. See the [API documentation](https://docs.databricks.com/dev-tools/api/latest/workspace.html#export) for return specification 

```python
workspace_export(from_path: str, format: Format, to_path: str) -> dict
```

## workspace_dir_exists

Predicate function to check if a workspace directory exists.

```python
workspace_dir_exists(path: str) -> bool
```

## workspace_notebook_exists

Predicate function to check if a notebook  exists.

```python
workspace_notebook_exists(path: str) -> bool
```



