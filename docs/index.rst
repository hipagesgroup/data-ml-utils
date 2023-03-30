.. data_ml_utils documentation master file, created by
   sphinx-quickstart on Sun Apr 24 16:49:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

data-ml-utils
+++++++++++++

This python library package covers the common utility packages that data/ml project will use

data-ml-utils has a few utilities that we try to generalise across projects.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   commands/pyathena
   commands/pyathena_api_specs
   commands/pyathena_utils_api_specs
   commands/databricks_utils_api_specs
   commands/mlflow_tracker_databricks
   commands/mlflow_tracker_databricks_api_specs
   commands/mlflow_utils_databricks
   commands/mlflow_utils_databricks_api_specs
   commands/mlflow_serve
   commands/mlflow_serve_api_specs
   commands/mlflow_prediction_requests
   commands/mlflow_prediction_requests_api_specs

Why are packaging this into a python library?
---------------------------------------------

There are utilities that are copied and pasted across different repositories (and projects), and we can streamline this to a package import.

Also, this would allow us to save some time by writing lesser tests.

Additionally, this would align the way how analysts query with athena through python too.


Getting Started
---------------

You can install `data-ml-utils` from the git repo using pip

.. code-block:: console

   $ pip install data-ml-utils --upgrade


Pyathena
--------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:

- query athena tables and return as pandas dataframe
- drop athena tables from offline feature store
- create athena tables through schema, and update table with missing partitions

See :doc:`commands/pyathena` for more details.


MLflow tracker
--------------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:

- log artifact
- log and register a model
- log params
- log metrics

See :doc:`commands/mlflow_tracker_databricks` for more details.


MLflow utils
------------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:

- load model
- load artifact
- get mlflow model evaluation metrics
- get registered model run info and mlflow run_id
- mlflow promote model

See :doc:`commands/mlflow_utils_databricks` for more details.

MLflow serve
------------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:

- enable model endpoint
- get endpoint status
- get endpoint state status
- update databricks model endpoint compute config

See :doc:`commands/mlflow_serve` for more details.

MLflow prediction requests
--------------------------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:

- verify prediction of requests and expected
- post requests for integration tests

See :doc:`commands/mlflow_prediction_requests` for more details.
