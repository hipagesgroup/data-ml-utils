MLflow serve API Specs
~~~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **enable_endpoint** (`databricks_api_url, model_name, databricks_cluster_hostname, databricks_workspace_token, dbfs_table_path, model_version, request_time_out`)
     - creates and enable inference logging for model serving endpoint
     - :ref:`enable_endpoint`
   * -  **get_endpoint_state_status** (`artifact_uri, artifact_name, type_of_artifact`)
     - returns the state of the databricks model endpoint, example: READY
     - :ref:`get_endpoint_state_status`
   * -  **get_endpoint_status** (`databricks_api_url, model_name, databricks_cluster_hostname, databricks_workspace_token, polling_step, polling_max_tries, request_time_out`)
     - returns a boolean if databricks model endpoint status is ready
     - :ref:`get_endpoint_status`
   * -  **update_compute_config** (`databricks_api_url, model_name, databricks_cluster_hostname, databricks_workspace_token, workload_size_id, model_version, scale_to_zero_enabled, request_time_out`)
     - update the databricks endpoint compute config of a registered model; cluster size, if it scales to zero and the % of traffic that flows through serving endpoint
     - :ref:`update_compute_config`


.. _enable_endpoint:

enable_endpoint
---------------
.. py:function:: enable_endpoint(databricks_api_url: str, model_name: str, databricks_cluster_hostname: str, databricks_workspace_token: str, dbfs_table_path: str, model_version: int, request_time_out:int = 60,)
   enable databricks model endpoint of a registered model (any model in Staging or Production tag gets deployed)

   :param databricks_api_url: url of the databricks api
   :type databricks_api_url: str
   :param model_name: name of registered model in mlflow
   :type model_name: str
   :param databricks_cluster_hostname: databricks cluster hostname; https://xxx.cloud.databricks.com
   :type databricks_cluster_hostname: str
   :param databricks_workspace_token: databricks workspace PAT
   :type databricks_workspace_token: str
   :param dbfs_table_path: dbfs file path for inference logging table
   :type dbfs_table_path: str
   :param model_version: registered model version of specified stage tag
   :type model_version: int
   :param request_time_out: duration before request times out, default at 60 seconds
   :type request_time_out: int
   :return: returns a boolean if the model is enabled
   :rtype: bool

.. _get_endpoint_state_status:

get_endpoint_state_status
-------------------------
.. py:function:: get_endpoint_state_status(response_json: dict,)
   returns the state of the databricks model endpoint, example: READY

   :param response_json: response of the get request of mlflow api of get-status
   :type response_json: dict
   :return: returns the state of the endpoint, example: READY
   :rtype: str

.. _get_endpoint_status:

get_endpoint_status
-------------------
.. py:function:: get_endpoint_status(databricks_api_url: str, model_name: str, databricks_cluster_hostname: str, databricks_workspace_token:str, polling_step: int = 10, polling_max_tries: int = 42, request_time_out:int = 60,)
   returns a boolean if databricks model endpoint status is ready

   :param databricks_api_url: url of the databricks api
   :type databricks_api_url: str
   :param model_name: name of registered model in mlflow
   :type model_name: str
   :param databricks_cluster_hostname: databricks cluster hostname; https://xxx.cloud.databricks.com
   :type databricks_cluster_hostname: str
   :param databricks_workspace_token: databricks workspace PAT
   :type databricks_workspace_token: str
   :param polling_step: duration of polling interval in seconds
   :type polling_step: int
   :param polling_max_tries: maximum number of tries of polling
   :type polling_max_tries: int
   :param request_time_out: duration before request times out, default at 60 seconds
   :type request_time_out: int
   :return: returns a boolean if the model is enabled
   :rtype: bool

.. _update_compute_config:

update_compute_config
---------------------
.. py:function:: update_compute_config(databricks_api_url: str, model_name: str, databricks_cluster_hostname: str, databricks_workspace_token:str, workload_size_id: str = 10, scale_to_zero_enabled: str, model_version: int, request_time_out:int = 60,)
   update the databricks endpoint compute config of a registered model; cluster size and if it scales to zero

   :param databricks_api_url: url of the databricks api
   :type databricks_api_url: str
   :param model_name: name of registered model in mlflow
   :type model_name: str
   :param databricks_cluster_hostname: databricks cluster hostname; https://xxx.cloud.databricks.com
   :type databricks_cluster_hostname: str
   :param databricks_workspace_token: databricks workspace PAT
   :type databricks_workspace_token: str
   :param workload_size_id: databricks model endpoint, size of cluster; Small, Medium or Large
   :type workload_size_id: str
   :param scale_to_zero_enabled: flag to scale to zero; true or false
   :type scale_to_zero_enabled: str
   :param model_version: registered model version of specified stage tag
   :type model_version: int
   :param request_time_out: duration before request times out, default at 60 seconds
   :type request_time_out: int
   :return: returns a non zero exit function if successful
   :rtype: int
