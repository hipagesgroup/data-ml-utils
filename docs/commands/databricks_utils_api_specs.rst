Databricks API Specs
~~~~~~~~~~~~~~~~~~~~

`Methods`

.. list-table::
   :widths: 100 50 50

   * -  **load_yaml** (`path`)
     - load yaml file
     - :ref:`load_yaml`
   * -  **get_test_date** (`file_path`)
     - get date from `x` days ago from specified date
     - :ref:`get_test_date`

.. _load_yaml:

load_yaml
---------
.. py:function:: load_yaml(path: str)
   load yaml file

   :param path: filepath of yaml file
   :type load yaml file: str
   :return: yaml contents as dictionary
   :rtype: Dict

.. _get_test_date:

get_test_date
-------------
.. py:function:: get_test_date(datetime_provided: datetime.datetime, days_difference: int)
   get date from `x` days ago from specified date

   :param datetime_provided: datetime input, most likely datetime.datetime.now()
   :type datetime_provided: datetime.datetime
   :param days_difference: number days ago we should look back
   :type days_difference: int
   :return: returns a date dim key, yyyyMMdd
   :rtype: int
