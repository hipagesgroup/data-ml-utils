Pyathena Utils API Specs
~~~~~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **read_sql** (`file_path`)
     - read sql file
     - :ref:`read_sql`
   * -  **get_config_yaml** (`file_path`)
     - get table schema config
     - :ref:`get_config_yaml`
   * -  **format_sql_create_schema** (`sql, yaml_file_path`)
     - create table sql from config schema
     - :ref:`format_sql_create_schema`
   * -  **format_sql_repair_table** (`sql, table_name`)
     - create repair table sql
     - :ref:`format_sql_repair_table`

.. _read_sql:

read_sql
--------
.. py:function:: read_sql(file_path: str)
   read sql file

   :param filepath: filepath of sql file
   :type filepath: str
   :return: sql query
   :rtype: str

.. _get_config_yaml:

get_config_yaml
---------------
.. py:function:: get_config_yaml(file_path: str)
   get table schema config

   :param filepath: filepath; of sql file
   :type filepath: str
   :return table_name: name of table
   :rtype: str
   :return: table_description; description of table
   :rtype: str
   :return: table_column_name; table column names
   :rtype: str
   :return: partition_column; name of partitioned column
   :rtype: str
   :return: partition_column_comment; description of partitioned column
   :rtype: str
   :return: s3_bucket name; of s3 bucket
   :rtype: str


.. _format_sql_create_schema:

format_sql_create_schema
------------------------
.. py:function:: format_sql_create_schema(sql: str, yaml_file_path: str)
   create table sql from config schema

   :param sql: sql query
   :type sql: str
   :param yaml_file_path: schema file path
   :type yaml_file_path: str
   :return: return_sql; final sql to create table
   :rtype: str
   :return: table_name; name of table
   :rtype: str


.. _format_sql_repair_table:

format_sql_repair_table
-----------------------
.. py:function:: format_sql_repair_table(sql: str, table_name: str)
   create repair table sql

   :param sql: sql query
   :type sql: str
   :param table_name: name of table to repair
   :type table_name: str
   :return: repair sql
   :rtype: str
