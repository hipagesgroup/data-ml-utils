import datetime
from unittest.mock import patch

from data_ml_utils.core.databricks_utils import get_test_date
from data_ml_utils.core.databricks_utils import load_yaml


class TestCommonUtils:
    """
    test class for common utils
    """

    @patch("yaml.safe_load")
    @patch("builtins.open")
    def test_load_yaml(self, mock_open, mock_safe_load) -> None:
        """
        function to test if load_settings() runs correctly

        Parameters
        ----------
        mock_open:
            mock builtins.open
        mock_safe_load:
            mock yaml.safe_load
        """

        expected_dict = {
            "test": "test",
            "test2": "test2",
        }
        mock_safe_load.return_value = expected_dict
        returned_dict = load_yaml("test")
        assert isinstance(returned_dict, dict)  # noqa: S101
        assert returned_dict == expected_dict  # noqa: S101

    def test_get_test_date(self) -> None:
        """
        test function to get test date

        Returns
        -------
        assert
            returns expected date dim key
        """

        datetime_value = datetime.datetime(2023, 3, 20, 14, 30, 48, 890521)
        expected_return = get_test_date(
            datetime_provided=datetime_value, days_difference=21
        )
        assert expected_return == 20230227  # noqa: S101
