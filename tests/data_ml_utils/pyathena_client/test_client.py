import pandas as pd
import pyathena
from mock import patch

from data_ml_utils.pyathena_client.client import PyAthenaClient


class TestPyAthenaClient:
    """test class for pyathena client"""

    @patch("data_ml_utils.pyathena_client.client.connect")
    def test_connect(self, mocked_pyathena, aws_credentials):
        """
        test function to connect to pyathena
        Parameters
        ----------
        mock_pyathena
            mocked pyathena connect
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            instance is athena connection
        """

        dummy_connection = pyathena.connect(
            s3_staging_dir=(
                """s3://au-com-hipages-offline-feature-store/athena_queries/"""
                """query_2019-01-01"""
            ),
            region_name="ap-southeast-2",
        )

        mocked_pyathena.return_value = dummy_connection

        test_client = PyAthenaClient()

        return_connection = test_client.engine

        assert isinstance(return_connection, pyathena.connection.Connection)

    @patch("data_ml_utils.pyathena_client.client.read_sql")
    @patch("data_ml_utils.pyathena_client.client.format_sql_create_schema")
    @patch("data_ml_utils.pyathena_client.client.format_sql_repair_table")
    def test_create_msck_repair_table_error(
        self,
        mocked_repair_table,
        mocked_create_schema,
        mocked_read_sql,
        aws_credentials,
    ):
        """
        test function for erraneous creating and repairing athena table
        Parameters
        ----------
        mocked_repair_table
            mocked repair table sql function
        mocked_create_schema
            mocked create schema sql function
        mocked_read_sql
            mocked read sql function
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            return value is 1
        """

        mocked_repair_table.return_value = "query_repair"
        mocked_create_schema.return_value = ("query", "table_test_name")
        mocked_read_sql.return_value = "query"

        # let it assume the default aws_creds which is invalid
        test = PyAthenaClient().create_msck_repair_table(
            create_raw_query="test.sql",
            repair_raw_query="test.sql",
            yaml_schema_file_path="test.yaml",
        )

        assert test == 1

    @patch("data_ml_utils.pyathena_client.client.read_sql")
    @patch("data_ml_utils.pyathena_client.client.format_sql_create_schema")
    @patch("data_ml_utils.pyathena_client.client.format_sql_repair_table")
    @patch("data_ml_utils.pyathena_client.client.PyAthenaClient")
    def test_create_msck_repair_table(
        self,
        mocked_pyathena,
        mocked_repair_table,
        mocked_create_schema,
        mocked_read_sql,
        aws_credentials,
    ):
        """
        test function for creating and repairing athena table
        Parameters
        ----------
        mocked_pyathena
            mocked pyathena client
        mocked_repair_table
            mocked repair table sql function
        mocked_create_schema
            mocked create schema sql function
        mocked_read_sql
            mocked read sql function
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            return value is 0
        """

        mocked_pyathena.cursor.return_value.execute.return_value = True
        mocked_repair_table.return_value = "query_repair"
        mocked_create_schema.return_value = ("query", "table_test_name")
        mocked_read_sql.return_value = "query"

        test_client = PyAthenaClient()
        # patch engine with mocked pyathena
        test_client.engine = mocked_pyathena

        test = test_client.create_msck_repair_table(
            create_raw_query="test.sql",
            repair_raw_query="test.sql",
            yaml_schema_file_path="test.yaml",
        )

        assert test == 0

    def test_drop_table_error(
        self,
        aws_credentials,
    ):
        """
        test function for erraneous creating and repairing athena table
        Parameters
        ----------
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            return value is 1
        """

        # let it assume the default aws_creds which is invalid
        test = PyAthenaClient().drop_table(
            table_name="test_table",
            database="whatever",
        )

        assert test == 1

    @patch("data_ml_utils.pyathena_client.client.PyAthenaClient")
    def test_drop_table(
        self,
        mocked_pyathena,
        aws_credentials,
    ):
        """
        test function for creating and repairing athena table
        Parameters
        ----------
        mocked_pyathena
            mocked pyathena client
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            return value is 0
        """

        mocked_pyathena.cursor.return_value.execute.return_value = True

        test_client = PyAthenaClient()
        # patch engine with mocked pyathena
        test_client.engine = mocked_pyathena

        test = test_client.drop_table(
            table_name="test_table",
            database="whatever",
        )

        assert test == 0

    @patch("data_ml_utils.pyathena_client.client.PyAthenaClient")
    def test_query_as_pandas(
        self,
        mocked_pyathena,
        aws_credentials,
    ):
        """
        test function for creating and repairing athena table
        Parameters
        ----------
        mocked_pyathena
            mocked pyathena client
        aws_credentials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            return value is a dataframe
        assert
            datatypes of dataframe columns are correct
        """

        dummy_df = pd.concat(
            [
                pd.Series([1, 2], dtype=pd.Int64Dtype()),
                pd.Series([1.0, 2.0], dtype=pd.Float64Dtype()),
            ],
            axis=1,
        )

        mocked_pyathena.cursor.return_value.execute.return_value.as_pandas.return_value = (  # noqa E501
            dummy_df
        )

        test_client = PyAthenaClient()
        # patch engine with mocked pyathena
        test_client.engine = mocked_pyathena

        test = test_client.query_as_pandas(final_query="testquery")

        assert isinstance(test, pd.DataFrame)
        assert test[0].dtype == int
        assert test[1].dtype == float
