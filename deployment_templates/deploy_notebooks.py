import os, sys
from uuid import uuid4

os.environ["DATABRICKS_API_HOST"] = sys.argv[1]
os.environ["DBUTILSTOKEN"] = sys.argv[2]
from_notebook_root = sys.argv[3]
source_dir = sys.argv[4]
target_dir = sys.argv[5]

# autobricks requires environment variables to be set
# must be imported here
from autobricks.Workspace import *

if workspace_dir_exists(target_dir):
     workspace_delete(target_dir, True)

result = workspace_mkdirs(target_dir)
result = workspace_import_dir(from_notebook_root, source_dir, target_dir, DeployMode.PARENT)
result = workspace_dir_exists(target_dir)