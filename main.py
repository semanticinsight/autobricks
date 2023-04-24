import os
from autobricks import Job
import yaml

ROOT_DIR = os.getenv("ROOT_DIR")


path = os.path.join(ROOT_DIR, "Databricks/Workflows/" "workflow.yaml")


with open(path, "r", encoding="utf-8")as f:
    data = yaml.safe_load(f)

name = data["name"]

Job.job_recreate(data)
