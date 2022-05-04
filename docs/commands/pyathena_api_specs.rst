Pyathena API Specs
~~~~~~~~~~~~~~~~~~

.. _init:

data_ml_utils.pyathena_client.client.PyAthenaClient
---------------------------------------------------
.. py:class:: data_ml_utils.pyathena_client.client.PyAthenaClient(kind=None)
   Initialises pyathena connection.

   :param kind: None.

The `PyAthenaClient` class does not take in any parameters to initialise it.

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **__init__** ()
     - initialise self
     - :ref:`init`
   * -  **_connect** ()
     - create pyathena connection
     - :ref:`connect`
   * -  **create_msck_repair_table** (`create_raw_query, repair_raw_query, yaml_schema_file_path`)
     - create and repair table through defined schema
     - :ref:`create_msck_repair_table`
   * -  **drop_table** (`table_name, database`)
     - drop table
     - :ref:`drop_table`
   * -  **query_as_pandas** (`final_query`)
     - query athena tables and return as pandas dataframe
     - :ref:`query_as_pandas`

.. _connect:

_connect
--------
.. py:function:: _connect()
   create a pyathena connection with pandas cursor

   :param kind: None.
   :return: pyathena connection engine
   :rtype: pyathena.connection.Connection

.. _create_msck_repair_table:

create_msck_repair_table
------------------------
.. py:function:: create_msck_repair_table(create_raw_query: str, repair_raw_query: str, yaml_schema_file_path: str)
   create table and msck repair table in athena with pyathena connection

   :param create_raw_query: create table raw sql query
   :type create_raw_query: str
   :param repair_raw_query: repair table raw sql query
   :type repair_raw_query: str
   :param yaml_schema_file_path: file path to yaml schema
   :type yaml_schema_file_path: str
   :return: non exit function value if successful
   :rtype: int

.. _drop_table:

drop_table
------------------------
.. py:function:: drop_tables(table_name: str, database: str)
   drop table in athena with pyathena connection

   :param table_name: table name
   :type table_name: str
   :param database: database name
   :type database: str
   :return: non exit function value if successful
   :rtype: int

.. _query_as_pandas:

query_as_pandas
------------------------
.. py:function:: query_as_pandas(final_query: str)
   query athena sqls with pyathena connection and store them into pandas

   :param table_name: table name
   :type table_name: str
   :param database: database name
   :type database: str
   :return: return of pandas dataframe
   :rtype: pd.DataFrame
