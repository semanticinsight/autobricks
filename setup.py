import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "PYPI.md").read_text()

# This call to setup() does all the work
setup(
    name="autobricks",
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}",
        "dirty_template": "{tag}.dev{ccount}.dirty",
        "starting_version": "0.0.1",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
    setup_requires=['setuptools-git-versioning'],
    description="Databricks Deployment Utils",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://autobricks.readthedocs.io/en/latest/",
    project_urls={
        'GitHub': 'https://github.com/semanticinsight/autobricks',
        'Documentation': 'https://autobricks.readthedocs.io/en/latest/'
    },
    author="Shaun Ryan",
    author_email="shaun_chiburi@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["autobricks"],
    install_requires=[
          'requests',
          'PyYAML'
      ],
    zip_safe=False
)
