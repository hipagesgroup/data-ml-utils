Client boto3 SageMaker API Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _init_sagemaker:

data_ml_utils.boto3_botocore_client.client_sagemaker.AwsSagemakerServices
-------------------------------------------------------------------------
.. py:class:: data_ml_utils.boto3_botocore_client.client_sagemaker.AwsSagemakerServices()
   Initialises sagemaker client.

   :param : None.

The `AwsSagemakerServices` class does not take in any parameters to initialise it.

`Methods`

.. list-table::
   :widths: 100 40 20

   * -  **__init__** ()
     - initialise self
     - :ref:`init_sagemaker`
   * -  **get_model_uri_from_aws_model_registry** (`model_name`)
     - retrieve approved model artefact uri from AWS model registry
     - :ref:`get_model_uri`
   * -  **unzip_targz_file** (`file_targz, bucket_name_trunc, targz_file_uri, s3_file_path`)
     - unzip model artefact file
     - :ref:`unzip_targz_file`
   * -  **upload_retrained_model_s3** (`date_format, bucket_name_trunc, s3_file_path, model_suffix`)
     - upload model artefact to s3
     - :ref:`upload_retrained_model_s3`
   * -  **create_model_package_version** (`model_name, model_file_name,`
        `current_retrained_model_metrics_dict, s3_directory,image_uri,model_package_description`)
     - create model package version in AWS model registry
     - :ref:`create_model_package_version`

.. _get_model_uri:

get_model_uri_from_aws_model_registry
-------------------------------------
.. py:function:: get_model_uri_from_aws_model_registry(model_name: str)
   retrieve approved model artefact uri from AWS model registry

   :param model_name: name of model group in AWS model registry
   :type model_name: str
   :return: targz_file_uri; model artefact uri
   :rtype: str
   :return: file; filename of model artefact
   :rtype: str

.. _unzip_targz_file:

unzip_targz_file
----------------
.. py:function:: unzip_targz_file(file_targz: str, bucket_name_trunc: str, targz_file_uri: str, s3_file_path: str)
   unzip model artefact file

   :param file_targz: filename of model artefact
   :type file_targz: str
   :param bucket_name_trunc: truncated s3 bucket directory
   :type bucket_name_trunc: str
   :param targz_file_uri: model artefact uri
   :type targz_file_uri: str
   :param s3_file_path: file path to file in s3 bucket
   :type s3_file_path: str
   :return: non exit function value if successful
   :rtype: int

.. _upload_retrained_model_s3:

upload_retrained_model_s3
-------------------------
.. py:function:: upload_retrained_model_s3(date_format: str, bucket_name_trunc: str, s3_file_path: str, model_suffix: str)
   upload model artefact to s3

   :param date_format: date format for file name
   :type date_format: str
   :param bucket_name_trunc: truncated s3 bucket directory
   :type bucket_name_trunc: str
   :param s3_file_path: file path to file in s3 bucket
   :type s3_file_path: str
   :param model_suffix: model file name suffix
   :type model_suffix: str
   :return: model_file_name; model artefact filename
   :rtype: str

.. _create_model_package_version:

create_model_package_version
----------------------------
.. py:function:: create_model_package_version(
        model_name: str,
        model_file_name: str,
        current_retrained_model_metrics_dict: str,
        s3_directory: str,
        image_uri: str,
        model_package_description: str
   )
   create model package version in AWS model registry

   :param model_name: model group name
   :type model_name: str
   :param model_file_name: model artefact filename
   :type model_file_name: str
   :param current_retrained_model_metrics_dict: evaluation metrics of retrained and current model
   :type current_retrained_model_metrics_dict: Dict
   :param s3_directory: s3 directory
   :type s3_directory: str
   :param image_uri: model ecr image uri
   :type image_uri: str
   :param model_package_description: model package description
   :type model_package_description: str
   :return: non exit function value if successful
   :rtype: int
