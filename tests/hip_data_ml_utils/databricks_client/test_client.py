from unittest.mock import MagicMock
from unittest.mock import patch

from databricks.sql import connect


class TestDatabricksSQLClient:
    """test class for databricks sql client"""

    @patch("hip_data_ml_utils.databricks_client.client.connect")
    def test_connect(self, mocked_databricks):
        """
        test function to connect to pyathena
        Parameters
        ----------
        mocked_databricks
            mocked databricks sql connect

        Returns
        -------
        assert
            instance is athena connection
        """

        mock_connection = MagicMock()
        mocked_databricks.return_value = mock_connection

        DUMMY_CONNECTION_ARGS = {
            "server_hostname": "foo",
            "http_path": "dummy_path",
            "access_token": "tok",
        }

        _ = connect(**DUMMY_CONNECTION_ARGS)

        mocked_databricks.assert_called_with(**DUMMY_CONNECTION_ARGS)
