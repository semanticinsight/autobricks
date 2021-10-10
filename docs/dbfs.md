# Dbfs

This module contains functions to working with databricks Dbfs storage.



## dbfs_upload

Uploads a file from a local path to dbfs destination path. `Overrite=True` will overwrite the file.

```python
dbfs_upload(from_path: str, to_path: str, overwrite: bool = True)
```

## dbfs_upload

Uploads all files matching a regex from a local path to dbfs destination path. `Overrite=True` will overwrite the file.

```python
dbfs_upload(file_match:str, from_path: str, to_path: str, overwrite: bool = True)
```

## [dbfs_delete_file](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#delete)

Deletes a file or folder at the Dbfs path provided. `recursive=True` is required for a directory.

```python
dbfs_delete_file(path: str, recursive: bool = True)
```

## [dbfs_get_status](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#get-status)

Get the file information of a file or directory. If the file or directory does not exist, this call throws an exception with RESOURCE_DOES_NOT_EXIST.

```python
dbfs_get_status(path: str)->dict
```

[See return dictionary](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#response-structure)

## [dbfs_list](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#list)

List the contents of a directory, or details of the file. If the file or directory does not exist, this call throws an exception with RESOURCE_DOES_NOT_EXIST.

```python
dbfs_list(path: str)->dict
```

[See return definition](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#response-structure)

## [dbfs_mkdirs](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#mkdirs)

Create the given directory and necessary parent directories if they do not exist. If there exists a file (not a directory) at any prefix of the input path, this call throws an exception with RESOURCE_ALREADY_EXISTS. If this operation fails it may have succeeded in creating some of the necessary parent directories.

```python
dbfs_mkdirs(path: str)
```

## [dbfs_move](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#move)

Move a file from one location to another location within DBFS. If the source file does not exist, this call throws an exception with RESOURCE_DOES_NOT_EXIST. If there already exists a file in the destination path, this call throws an exception with RESOURCE_ALREADY_EXISTS. If the given source path is a directory, this call always recursively moves all files.

```python
dbfs_move(source_path: str, destination_path: str)
```

## [dbfs_read](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#read)

Return the contents of a file. If the file does not exist, this call throws an exception with RESOURCE_DOES_NOT_EXIST. If the path is a directory, the read length is negative, or if the offset is negative, this call throws an exception with INVALID_PARAMETER_VALUE. If the read length exceeds 1 MB, this call throws an exception with MAX_READ_SIZE_EXCEEDED. If offset + length exceeds the number of bytes in a file, reads contents until the end of file.

```python
dbfs_read(path: str, offset: int, length: int)
```

[See return definition](https://docs.databricks.com/dev-tools/api/latest/dbfs.html#response-structure)


## dbfs_download

Download a file from the dbfs path to local path. Note this downloads a file in 1mb chunks using a binary offset.

```python
dbfs_download(from_path: str, to_path: str)
```

## find_file

Find files matching a `pattern` recursively under under a `directory` path. Returns a list of files paths.

```python
find_file(pattern: str, path: str)->list
```



