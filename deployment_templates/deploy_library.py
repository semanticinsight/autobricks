import os, fnmatch, sys


os.environ["DATABRICKS_API_HOST"] = sys.argv[1]
os.environ["DBUTILSTOKEN"] = sys.argv[2]
print(os.getcwd())

from autobricks import Workspace, Job, Dbfs
from uuid import uuid4
from pprint import pprint


filename = "autobricks-*-py3-none-any.whl"
build_dir = sys.argv[3]
deploy_dir = sys.argv[4] 


Dbfs.dbfs_upload_files('*.whl', build_dir, deploy_dir, True)

