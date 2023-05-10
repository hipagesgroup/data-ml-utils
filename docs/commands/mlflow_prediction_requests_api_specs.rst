MLflow prediction requests API Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **verify_prediction** (`response_json, expected_keywords_response,`)
     - verifies if a prediction output is as expected
     - :ref:`verify_prediction`
   * -  **get_requests** (`model_name, databricks_cluster_hostname, databricks_workspace_token, settings, keywords, request_time_out`)
     - makes post requests for model inference and verify that inference is within expectations
     - :ref:`get_requests`

.. _verify_prediction:

verify_prediction
-----------------
.. py:function:: verify_prediction(response_json: dict, expected_keywords_response: str,)
   load an ML model from MLflow run, raises an exception if type_of_model is not in dictionary

   :param response_json: json response of the post request from model endpoint
   :type response_json: dict
   :param expected_keywords_response: expected top parent seo name for keywords
   :type expected_keywords_response: str
   :return: non exit response if response matches
   :rtype: bool

.. _get_requests:

get_requests
------------
.. py:function:: get_requests(model_name: str, databricks_cluster_hostname: str, databricks_workspace_token: str, settings: dict, keywords: str, request_time_out: int = 60,)
   load an artifact from MLflow run, accepts `joblib, pkl, dict and yaml` file types

   :param model_name: name of the registered model
   :type model_name: str
   :param databricks_cluster_hostname: hostname of the databricks cluster
   :type databricks_cluster_hostname: str
   :param databricks_workspace_token: token of the databricks workspace
   :type databricks_workspace_token: str
   :param settings: repo settings and configuration
   :type settings: dict
   :param keywords: keywords to be used for prediction
   :type keywords: str
   :param request_time_out: time out for the request
   :type request_time_out: int
   :return: returns a callable python object; dictionary, pandas dataframe, list
   :rtype: int
