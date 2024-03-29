import datetime
from typing import Callable
from unittest.mock import patch

from hip_data_ml_utils.core.databricks_utils import get_date_intervals_model_drift
from hip_data_ml_utils.core.databricks_utils import get_function_to_load
from hip_data_ml_utils.core.databricks_utils import get_target_stage_for_env
from hip_data_ml_utils.core.databricks_utils import get_test_date
from hip_data_ml_utils.core.databricks_utils import load_yaml


class TestDatabricksCommonUtils:
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

    def test_get_function_to_load(self, dummy_function_dict) -> None:
        """
        test get function loader works correctly

        Parameters
        ----------
        dummy_function_dict
            dummy function dictionary

        Returns
        -------
        assert
            returns True that the callable is the correct instance
        """

        return_function = get_function_to_load(
            function_dict=dummy_function_dict,
            file_format="pkl",
        )

        assert isinstance(return_function, Callable)  # noqa: S101

    def test_get_target_stage_for_env(self) -> None:
        """
        test function for returning env

        Returns
        -------
        assert
            returns True that the env is as expected
        """

        assert get_target_stage_for_env("dev") == "Staging"  # noqa: S101
        assert get_target_stage_for_env("staging") == "Staging"  # noqa: S101
        assert get_target_stage_for_env("prod") == "Production"  # noqa: S101

    def test_get_date_intervals_model_drift(
        self,
    ) -> None:
        """
        test get date intervals works correctly

        Returns
        -------
        assert
            returns True that list is the same
        """

        expected_list = get_date_intervals_model_drift(
            date_int=20230701,
        )

        assert expected_list[0] == "20230701_hour_pair_1"  # noqa: S101
        assert expected_list[-1] == "20230701_hour_pair_4"  # noqa: S101
