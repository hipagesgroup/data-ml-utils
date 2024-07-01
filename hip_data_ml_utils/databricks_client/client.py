from __future__ import annotations

import os

import databricks
import pandas as pd
from databricks.sql import connect


class DatabricksSQLClient:
    """
    Class that handles queries from databricks sql connector
    Main purpose is to create a connection we can query from databricks sql warehouse
    """

    def __init__(self):
        self.engine = self._connect()

    def _connect(self) -> databricks.sql.client.Connection:
        """
        create a databricks sql connection

        Returns
        -------
        databricks.sql.client.Connection
            databricks sql warehouse connection engine
        """

        return connect(
            server_hostname=os.environ["DATABRICKS_HOST"],
            http_path=os.environ["DATABRICKS_SQL_PATH"],
            access_token=os.environ["DATABRICKS_TOKEN"],
        )

    def query_as_pandas(self, final_query: str) -> pd.DataFrame:
        """
        query databricks sqls with databricks connection and store them into pandas

        Parameters
        ----------
        final_query : str
            query to run

        Returns
        -------
        pd.DataFrame
            return of pandas dataframe
        """

        _cursor = self.engine.cursor()
        return_values = _cursor.execute(final_query).fetchall()

        return pd.DataFrame(
            return_values, columns=[col[0] for col in _cursor.description]
        )
