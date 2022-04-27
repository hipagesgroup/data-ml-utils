Client boto3 SageMaker API Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _init_emr:

data_ml_utils.boto3_botocore_client.client_emr.AwsEMRServices
-------------------------------------------------------------------------
.. py:class:: data_ml_utils.boto3_botocore_client.client_emr.AwsEMRServices()
   Initialises EMR client.

   :param : None.

The `AwsEMRServices` class does not take in any parameters to initialise it.

`Methods`

.. list-table::
   :widths: 100 40 20

   * -  **__init__** ()
     - initialise self
     - :ref:`init_emr`
   * -  **create_emr_cluster** (`master_instance_type, core_instance_type,`
        `core_instance_count, configurations,`
        `applications, log_uri, task_id, identifier, bidprice`)
     - creates EMR cluster
     - :ref:`create_emr_cluster`
   * -  **check_emr_cluster_status** (`cluster_id`)
     - check emr cluster that is created
     - :ref:`check_emr_cluster_status`
   * -  **terminate_emr_cluster** (`cluster_id`)
     - terminate created cluster
     - :ref:`terminate_emr_cluster`
   * -  **get_cluster_id** (`task_id, identifier`)
     - retrieve cluster identifier string value
     - :ref:`get_cluster_id`
   * -  **get_emr_master_dns_name** (`cluster_id`)
     - retrieve cluster master node dns address
     - :ref:`get_emr_master_dns_name`
   * -  **spin_up_emr_cluster** (`master_instance_type, core_instance_type,`
        `core_instance_count, configurations,`
        `applications, log_uri, task_id, identifier, bidprice`)
     - wrapper function to spin up EMR cluster and checks EMR cluster status
     - :ref:`spin_up_emr_cluster`

.. _create_emr_cluster:

create_emr_cluster
------------------
.. py:function:: create_emr_cluster(
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str)
   creates EMR cluster

   :param master_instance_type: name of ec2 instance for master node
   :type master_instance_type: str
   :param core_instance_type: name of ec2 instance for slave nodes
   :type core_instance_type: str
   :param core_instance_count: number of slave instances
   :type core_instance_count: int
   :param configurations: configuration of EMR cluster
   :type configurations: List
   :param applications: applications for EMR cluster
   :type applications: List
   :param log_uri: s3 directory of loggings
   :type log_uri: str
   :param task_id: task identifier
   :type task_id: str
   :param identifier: date identifier of task
   :type identifier: str
   :param bidprice: bidprice of spot ec2 instances
   :type bidprice: str
   :return: response; response of API return
   :rtype: dict

.. _check_emr_cluster_status:

check_emr_cluster_status
------------------------
.. py:function:: check_emr_cluster_status(cluster_id: str)
   check emr cluster that is created

   :param cluster_id: identifier of cluster
   :type cluster_id: str
   :return: non exit function value if successful
   :rtype: int

.. _terminate_emr_cluster:

terminate_emr_cluster
---------------------
.. py:function:: terminate_emr_cluster(cluster_id: str)
   terminate created cluster

   :param cluster_id: identifier of cluster
   :type cluster_id: str
   :return: non exit function value if successful
   :rtype: int

.. _get_cluster_id:

get_cluster_id
--------------
.. py:function:: get_cluster_id(task_id: str, identifier: str)
   retrieve cluster identifier string value

   :param task_id: task identifer
   :type task_id: str
   :param identifier: task date identifier
   :type identifier: str
   :return: cluster_id; EMR cluster identifier
   :rtype: str

.. _get_emr_master_dns_name:

get_emr_master_dns_name
-----------------------
.. py:function:: get_emr_master_dns_name(cluster_id: str)
   retrieve cluster master node dns address

   :param cluster_id: identifier of cluster
   :type cluster_id: str
   :return: dns_name; EMR cluster master dns name
   :rtype: str

.. _spin_up_emr_cluster:

spin_up_emr_cluster
-------------------
.. py:function:: spin_up_emr_cluster(
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str)
   wrapper function to spin up EMR cluster and checks EMR cluster status

   :param master_instance_type: name of ec2 instance for master node
   :type master_instance_type: str
   :param core_instance_type: name of ec2 instance for slave nodes
   :type core_instance_type: str
   :param core_instance_count: number of slave instances
   :type core_instance_count: int
   :param configurations: configuration of EMR cluster
   :type configurations: List
   :param applications: applications for EMR cluster
   :type applications: List
   :param log_uri: s3 directory of loggings
   :type log_uri: str
   :param task_id: task identifier
   :type task_id: str
   :param identifier: date identifier of task
   :type identifier: str
   :param bidprice: bidprice of spot ec2 instances
   :type bidprice: str
   :return: non exit function value if successful
   :rtype: int
