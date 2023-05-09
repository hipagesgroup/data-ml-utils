MLflow utils Databricks API Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **mlflow_load_model** (`model_uri, type_of_model, model_func_dict`)
     - load an ML model from MLflow run, raises an exception if type_of_model is not in dictionary
     - :ref:`mlflow_load_model`
   * -  **mlflow_load_artifact** (`artifact_uri, artifact_name, type_of_artifact`)
     - load an artifact from MLflow run, accepts `joblib, pkl, dict and yaml` file types
     - :ref:`mlflow_load_artifact`
   * -  **mlflow_get_model_metrics** (`run_id, key_value_metrics`)
     - gets all model evaluation metrics logged in MLflow run, or a specified key value evaluation metric
     - :ref:`mlflow_get_model_metrics`
   * -  **mlflow_get_model_version** (`mlflow_client, name, stage`)
     - gets registered model version of "Staging" or "Production"
     - :ref:`mlflow_get_model_version`
   * -  **mlflow_get_both_registered_model_info_run_id** (`name, mlflow_client, run_id, stage`)
     - log model evaluation metrics to mlflow run
     - :ref:`mlflow_get_both_registered_model_info_run_id`
   * -  **mlflow_promote_model** (`name, retrained_run_id, retrained_metric, start_date, eval_date, env, mlflow_client, metrics_name, prev_run_id, prev_metric`)
     - log model evaluation metrics to mlflow run
     - :ref:`mlflow_promote_model`

.. _mlflow_load_model:

mlflow_load_model
-----------------
.. py:function:: mlflow_load_model(model_uri: str, type_of_model: str, model_func_dict: dict,)
   load an ML model from MLflow run, raises an exception if type_of_model is not in dictionary

   :param model_uri: model location uri from MLflow run
   :type model_uri: str
   :param type_of_model: name of type of model; `sk_model, pytorch, python_model, keras, etc`
   :type type_of_model: str
   :param model_func_dict: dictionary of allowed models to be loaded
   :type model_func_dict: dict
   :return: any allowed model callable
   :rtype: Any

.. _mlflow_load_artifact:

mlflow_load_artifact
--------------------
.. py:function:: mlflow_load_artifact(artifact_uri: str, artifact_name: str, type_of_artifact: str = "joblib",)
   load an artifact from MLflow run, accepts `joblib, pkl, dict and yaml` file types

   :param artifact_uri: artifact uri location from MLflow run
   :type artifact_uri: str
   :param artifact_name: name of artifact
   :type artifact_name: str
   :param type_of_artifact: filetype, accepts `joblib, pkl, dict and yaml` file types
   :type type_of_artifact: str
   :return: returns a callable python object; dictionary, pandas dataframe, list
   :rtype: Any

.. _mlflow_get_model_metrics:

mlflow_get_model_metrics
------------------------
.. py:function:: mlflow_get_model_metrics(run_id: str, key_value_metrics: str = None,)
   gets all model evaluation metrics logged in MLflow run, or a specified key value evaluation metric

   :param run_id: unique identifier of MLflow run
   :type run_id: str
   :param key_value_metrics: name of evaluation metric
   :type key_value_metrics: str
   :return: all of evaluation metric (Dict), or singular evaluation metric as float or int
   :rtype: Union[float, int, Dict]

.. _mlflow_get_model_version:

mlflow_get_model_version
------------------------
.. py:function:: mlflow_get_model_version(mlflow_client: mlflow.tracking.client.MlflowClient, name: str, stage: str = "Production")
   gets registered model version of "Staging" or "Production"

   :param mlflow_client: mlflow client
   :type mlflow_client: mlflow.tracking.client.MlflowClient
   :param name: name of model
   :type name: str
   :param stage: name of stage
   :type stage: str

.. _mlflow_get_both_registered_model_info_run_id:

mlflow_get_both_registered_model_info_run_id
--------------------------------------------
.. py:function:: mlflow_get_both_registered_model_info_run_id(name: str, mlflow_client: mlflow.tracking.client.MlflowClient, run_id: str = None, stage: str = "Production",)
   returns the registered model information from the specified MLflow run_id, and the MLflow run_id of the specified staging tag; Staging, Archived or Production

   :param name: name of model
   :type name: str
   :param mlflow_client: mlflow client
   :type mlflow_client: mlflow.tracking.client.MlflowClient
   :param run_id: unique identifier of MLflow run
   :type run_id: float
   :param stage: name of stage
   :type stage: str
   :return: run_id, registered model information
   :rtype: Tuple[str, Dict]

.. _mlflow_promote_model:

mlflow_promote_model
--------------------
.. py:function:: mlflow_promote_model(name: str, retrained_run_id: str, retrained_metric: float, start_date: str, eval_date: str, env: str, mlflow_client: mlflow.tracking.client.MlflowClient, metrics_name: str, prev_run_id: str = None, prev_metric: float = 0.0,)
   function that decides if we need to promote model to the staging tag if there is no model in the specified staging tag, and

   :param key: name of evaluation metric
   :type key: str
   :param retrained_run_id: unique identifier of retrained MLflow run
   :type retrained_run_id: str
   :param retrained_metric: retrained model primary evaluation metric
   :type retrained_metric: float
   :param start_date: start date of dataset
   :type start_date: str
   :param eval_date: end date of dataset
   :type eval_date: str
   :param env: name of environment; `staging, dev, prod`
   :type env: str
   :param mlflow_client: initialised MLflow client
   :type mlflow_client: mlflow.tracking.client.MlflowClient
   :param metrics_name: name of evaluation metrics
   :type metrics_name: str
   :param prev_run_id: unique identifier of previous MLflow run
   :type prev_run_id: str
   :param prev_metric: previous MLflow run evaluation metric
   :type prev_metric: float
   :return: string response of the promotion of model
   :rtype: str
