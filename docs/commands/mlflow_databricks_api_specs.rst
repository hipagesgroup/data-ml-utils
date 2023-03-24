MLflow Databricks API Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **mlflow_log_artifact** (`file_path`)
     - log an artifact to mlflow run
     - :ref:`mlflow_log_artifact`
   * -  **mlflow_log_register_model** (`file_path`)
     - log and register model to mlflow run
     - :ref:`mlflow_log_register_model`
   * -  **mlflow_log_params** (`file_path`)
     - log model parameters to mlflow run
     - :ref:`mlflow_log_params`
   * -  **mlflow_log_metric** (`file_path`)
     - log model evaluation metrics to mlflow run
     - :ref:`mlflow_log_metric`

.. _mlflow_log_artifact:

mlflow_log_artifact
-------------------
.. py:function:: mlflow_log_artifact(artifact: Any, artifact_name: str, local_path: Optional[str] = None, artifact_path: Optional[str] = None)
   log an artifact to mlflow run

   :param artifact: artifact to log
   :type artifact: Any
   :param artifact_name: name of artifact
   :type artifact_name: str
   :param local_path: path to artifact
   :type local_path: Optional[str]
   :param artifact_path: directory to write artifact to for mlflow run
   :type artifact_path: Optional[str]
   :return: string response of the artifact logged
   :rtype: str

.. _mlflow_log_register_model:

mlflow_log_register_model
-------------------------
.. py:function:: mlflow_log_register_model(model, type_of_model: str, model_func_dict: dict, artifact_path: str, name_of_registered_model: str = None, extra_pip_requirements: Optional[list] = None, code_path: Optional[list] = None)
   log and register model to mlflow run

   :param model: model to log
   :param type_of_model: type of model; sklearn, tensorflow, pyfunc, pytorch
   :type type_of_model: str
   :param model_func_dict: mapping of dictionary for model function
   :type model_func_dict: dict
   :param artifact_path: artifact path
   :type artifact_path: str
   :param name_of_registered_model: name of registered model
   :type name_of_registered_model: str
   :param extra_pip_requirements: list of pip requirements for model
   :type extra_pip_requirements: Optional[list]
   :param code_path: list of code path for additional dependencies of model
   :type code_path: Optional[list]
   :return: string response of the model logged and registered
   :rtype: str

.. _mlflow_log_params:

mlflow_log_params
-----------------
.. py:function:: mlflow_log_params(params: dict)
   log model parameters to mlflow run

   :param params: parameters in dictionary to log
   :type params: str
   :return: string response of the params logged
   :rtype: str

.. _mlflow_log_metric:

mlflow_log_metric
-----------------
.. py:function:: mlflow_log_metric(key: str, value: float)
   log model evaluation metrics to mlflow run

   :param key: name of evaluation metric
   :type key: str
   :param value: evaluation metric value
   :type value: float
   :return: string response of the evaluation metric logged
   :rtype: str
