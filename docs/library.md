# Libary

This module contains functions to working with databricks Libaries.

## library_all_cluster_statuses

```python
library_all_cluster_statuses->list
```

Returns a list of [cluster library statuses](https://docs.databricks.com/dev-tools/api/latest/libraries.html#managedlibrariesclusterlibrarystatuses).

## get_latest_wheel

Gets the latest [PEP440](https://www.python.org/dev/peps/pep-0440/) semantic version of a wheel at a dir `path` based on the library `name`.

```python
get_latest_wheel(path: str, name: str)->Wheel
```

Returns a wheel object:

```python
@dataclass
class Wheel:
    path: str
    name: str
    major: int
    minor: int
    patch: int
    dev: int # incremental dev commit past the last release label
```