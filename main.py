# import os
# from autobricks import Job

# ROOT_DIR = os.getenv("ROOT_DIR")


# path = os.path.join(ROOT_DIR, "Databricks/Workflows/")

# Job.job_import_jobs(path)

from autobricks import Workspace

from_path = "./project_patterns"
to_path = "/project_patterns"

Workspace.workspace_import_dir(
    from_path=from_path,
    to_path=to_path,
    # sub_dirs=["databricks","pipelines"]
)