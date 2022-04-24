.. data_ml_utils documentation master file, created by
   sphinx-quickstart on Sun Apr 24 16:49:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

data-ml-utils
+++++++++++++

This python library package covers the common utility packages that data/ml project will use

.. image:: https://badge.fury.io/py/data-ml-utils.svg
    :target: https://github.com/hipagesgroup/data-ml-utils/tree/master

data-ml-utils has a few utilities that we try to generalise across projects.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   commands/pyathena
   commands/client_boto3

Why are packaging this into a python library?
---------------------------------------------

There are utilities that are copied and pasted across different repositories (and projects), and we can streamline this to a package import.

Also, this would allow us to save some time by writing lesser tests.

Additionally, this would align the way how analysts query with athena through python too.


Getting Started
---------------

You can install `data-ml-utils` from the git repo using pip

.. code-block:: console

   $ pip install git+ssh://git@github.com/hipagesgroup/data-ml-utils@v0.1.0


Pyathena
--------
We try to fit the function calls to be as simple as possible with a one-liner.
This covers:
- query athena tables and return as pandas dataframe
- drop athena tables from offline feature store
- create athena tables through schema, and update table with missing partitions

See :doc:`commands/pyathena` for more details.


Client boto3 and botocore
-------------------------
placeholder
