from __future__ import annotations

import datetime
import os

import pyathena
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

from core.config import settings
from core.utils import format_sql_create_schema
from core.utils import format_sql_repair_table
from core.utils import read_sql


class PyAthenaClient:
    """
    Class that handles queries from pyathena client
    Main purpose is to create a connection that we can query from
    """

    def __init__(self):
        self.engine = self._connect()

    def _connect(self) -> pyathena.connection.Connection:
        """
        create a pyathena connection with pandas cursor
        this queries athena queries much faster
        Returns
        -------
        pyathena.connection.Connection
            pyathena connection engine
        """
        today_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

        connection = connect(
            s3_staging_dir=f"{settings.S3_ATHENA_QUERY_DIRECTORY}query_{today_date}",
            region_name="ap-southeast-2",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            cursor_class=PandasCursor,
        )
        return connection

    def create_msck_repair_table(
        self, create_raw_query: str, repair_raw_query: str, yaml_schema_file_path: str
    ) -> int:
        """
        create table and msck repair table in athena with pyathena connection

        Parameters
        ----------
        create_raw_query : str
            raw query string to create table in athena
        repair_raw_query : str
            raw query string to repair table in athena
        yaml_schema_file_path : str
            yaml file path for schema of table to be created and repaired

        Returns
        -------
        int
            non exit function value if successful
        """

        create_schema_query_raw = read_sql(file_path=create_raw_query)
        repair_table_query_raw = read_sql(file_path=repair_raw_query)

        create_schema_query, table_name = format_sql_create_schema(
            sql=create_schema_query_raw, yaml_file_path=yaml_schema_file_path
        )

        repair_table_query = format_sql_repair_table(
            sql=repair_table_query_raw, table_name=table_name
        )

        try:
            self.engine.cursor().execute(create_schema_query)
            self.engine.cursor().execute(repair_table_query)
            return 0
        except Exception:
            return 1
