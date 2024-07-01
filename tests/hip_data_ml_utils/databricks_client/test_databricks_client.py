from unittest.mock import Mock
from unittest.mock import patch

from databricks import sql


class TestDatabricksSQLClient:
    """test class for databricks sql client"""

    def test_connect(self, dummy_client_args_dict):
        """
        test function to connect to pyathena
        Parameters
        ----------
        dummy_client_args_dict
            dummy client args dict

        Returns
        -------
        assert
            instance is athena connection
        """

        with patch("databricks.sql.connect", return_value=Mock()) as mock_connect:
            _ = sql.connect(**dummy_client_args_dict)
            mock_connect.assert_called_with(**dummy_client_args_dict)
