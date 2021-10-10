import sys
from autobricks import Dbfs

build_dir = sys.argv[3]
deploy_dir = sys.argv[4] 


Dbfs.dbfs_upload_files('*.whl', build_dir, deploy_dir, True)

