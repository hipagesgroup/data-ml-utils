from __future__ import annotations

import datetime
import os

import pandas as pd
import pyathena
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

from hip_data_ml_utils.core.config import settings
from hip_data_ml_utils.core.pyathena_utils import format_sql_create_schema
from hip_data_ml_utils.core.pyathena_utils import format_sql_repair_table
from hip_data_ml_utils.core.pyathena_utils import read_sql


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
            s3_staging_dir=f"{os.environ['S3_BUCKET']}query_{today_date}",
            region_name=settings.AWS_DEFAULT_REGION,
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

    def drop_table(self, table_name: str, database: str) -> int:
        """
        drop table in athena with pyathena connection

        Parameters
        ----------
        table_name : str
            raw query string to create table in athena
        database : str
            raw query string to repair table in athena

        Returns
        -------
        int
            non exit function value if successful
        """

        query = f"DROP TABLE IF EXISTS {database}.{table_name}"

        try:
            self.engine.cursor().execute(query)
            return 0
        except Exception:
            return 1

    def query_as_pandas(self, final_query: str) -> pd.DataFrame:
        """
        query athena sqls with pyathena connection and store them into pandas
        changes all pandas int and float types to numpy types

        Parameters
        ----------
        final_query : str
            query to run

        Returns
        -------
        pd.DataFrame
            return of pandas dataframe
        """

        return_df = self.engine.cursor().execute(final_query).as_pandas()

        # change all pandas Int64 and Float64 to numpy int and float
        for col in return_df.columns:
            if (
                ("Int" in str(return_df[col].dtype))
                and (return_df[col].isna().sum(axis=0) > 0)
            ) or ("Float" in str(return_df[col].dtype)):
                return_df[col] = return_df[col].astype(float)
            elif ("Int" in str(return_df[col].dtype)) and (
                return_df[col].isna().sum(axis=0) == 0
            ):
                return_df[col] = return_df[col].astype(int)

        return return_df
