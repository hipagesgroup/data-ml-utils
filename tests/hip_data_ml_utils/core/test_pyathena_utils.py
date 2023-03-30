import pathlib
from unittest.mock import mock_open
from unittest.mock import patch

from hip_data_ml_utils.core.pyathena_utils import format_sql_create_schema
from hip_data_ml_utils.core.pyathena_utils import format_sql_repair_table
from hip_data_ml_utils.core.pyathena_utils import get_config_yaml
from hip_data_ml_utils.core.pyathena_utils import read_sql


class TestReadSQL:
    """test class to read sql file"""

    @patch("pathlib.Path.open", new_callable=mock_open, read_data="test")
    def test_read_sql(self, mock_open_sql) -> None:
        """
        test function to read sql file

        Parameters
        ----------
        mock_open_sql
            mocked opening of sql files

        Returns
        -------
        assert
            contents inside file is the same
            if args taskid is the same
        """

        real_contents = read_sql("/dev/null")
        contents = pathlib.Path("/dev/null").read_text()
        assert contents == real_contents  # noqa: S101


class TestFormatSQL:
    """test class to get the formatted sql for create and repair table"""

    def test_get_config_yaml(self, dummy_test_table) -> None:
        """
        test function to get config yaml

        Parameters
        ----------
        dummy_test_table
            dummy table name

        Returns
        -------
        assert
            if return values are as expected
        """
        (
            table_name,
            table_description,
            table_column_name,
            partition_column,
            partition_column_comment,
            s3_bucket,
        ) = get_config_yaml("tests/hip_data_ml_utils/core/test_yaml.yaml")

        assert table_name == dummy_test_table  # noqa: S101
        assert s3_bucket == "testing-bucket/testing/"  # noqa: S101
        assert partition_column == "inference_date_created"  # noqa: S101

    @patch("hip_data_ml_utils.core.pyathena_utils.get_config_yaml")
    def test_format_sql_create_schema(
        self, mocked_config_function, dummy_test_table
    ) -> None:
        """
        test function to get sql create table schema

        Parameters
        ----------
        mocked_config_function
            mocked get config yaml function
        dummy_test_table
            dummy table name

        Returns
        -------
        assert
            if table name is as expected
        """

        mocked_config_function.return_value = (
            dummy_test_table,
            "table description",
            "test_column INT COMMENT 'test-description'",
            "date_created",
            "partition date",
            "test-bucket/testing/",
        )

        dummy_sql = """CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (\n    {table_column_name}\n)
            COMMENT {table_description}
            PARTITIONED BY ({partitioned_column} STRING COMMENT {partitioned_column_comment}) # noqa E501
            STORED AS PARQUET
            LOCATION {s3_bucket}
            tblproperties ("parquet.compression"="SNAPPY");"""

        return_sql, return_table_name = format_sql_create_schema(
            dummy_sql, "tests/data_ml_utils/core/test_yaml.yaml"
        )

        assert return_table_name == dummy_test_table  # noqa: S101

    def test_format_sql_repair_table(self, dummy_test_table) -> None:
        """
        test function to get sql create table schema

        Parameters
        ----------
        dummy_test_table
            dummy table name

        Returns
        -------
        assert
            if table name is as expected
            if sql return value is as expected
        """
        dummy_sql = "REPAIR TABLE {table_name}"

        dummy_table_name = dummy_test_table

        return_sql = format_sql_repair_table(dummy_sql, dummy_table_name)

        assert return_sql == "REPAIR TABLE dev.test_table"  # noqa: S101
