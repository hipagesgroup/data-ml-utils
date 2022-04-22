import datetime
import os

import pandas as pd
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor


class PyAthenaClient:
    def __init__(self):
        self.engine_pd = self._connect()
        self.engine = self._connect_faster()

    def _connect(self):
        today_date = pd.to_datetime(datetime.datetime.now()).strftime("%Y-%m-%d")

        connection = connect(
            s3_staging_dir=(
                """s3://au-com-hipages-offline-feature-store/athena_queries/"""
                f"""query_{today_date}"""
            ),
            region_name="ap-southeast-2",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        return connection

    def _connect_faster(self):
        today_date = pd.to_datetime(datetime.datetime.now()).strftime("%Y-%m-%d")

        connection = connect(
            s3_staging_dir=(
                """s3://au-com-hipages-offline-feature-store/athena_queries/"""
                f"""query_{today_date}"""
            ),
            region_name="ap-southeast-2",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            cursor_class=PandasCursor,
        )
        return connection

    def create_table(self, query: str) -> int:
        # create table if does not exist
        pd.read_sql(sql=query, con=self.engine_pd)

        return 0

    def msck_repair_table(self, query: str) -> int:
        # add missing partitions
        pd.read_sql(sql=query, con=self.engine_pd)

        return 0
