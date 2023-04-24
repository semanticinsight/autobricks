import os
from autobricks import Job
import yaml

ROOT_DIR = os.getenv("ROOT_DIR")


path = os.path.join(ROOT_DIR, "Databricks/Workflows/")

Job.job_import_jobs(path)