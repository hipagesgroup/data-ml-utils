from unittest.mock import MagicMock
from unittest.mock import patch

import pandas as pd
import pytest

from hip_data_ml_utils.mlflow_databricks.mlflow_model_utils import (
    mlflow_get_both_registered_model_info_run_id,
)
from hip_data_ml_utils.mlflow_databricks.mlflow_model_utils import (
    mlflow_get_model_metrics,
)
from hip_data_ml_utils.mlflow_databricks.mlflow_model_utils import mlflow_load_artifact
from hip_data_ml_utils.mlflow_databricks.mlflow_model_utils import mlflow_load_model
from hip_data_ml_utils.mlflow_databricks.mlflow_model_utils import mlflow_promote_model


class TestMlflowModelUtils:
    """
    test class for mlflow model-specific utilities
    """

    @patch("hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.getattr")
    def test_mlflow_load_model(self, mock_getattr) -> None:
        """
        test if mlflow_load_model() can load model

        Parameters
        ----------
        mock_model_func:
            mock patch getattr
        """

        mock_getattr.return_value = MagicMock()
        mlflow_load_model(
            model_uri="test_uri",
            type_of_model="test",
            model_func_dict={"test": "test"},
        )
        mock_getattr.assert_called_once()

    def test_mlflow_load_model_error(self) -> None:
        """
        test if mlflow_load_model() raises the right exception
        """

        with pytest.raises(ValueError, match="Model type not supported"):
            mlflow_load_model(
                model_uri="test_uri",
                type_of_model="invalid",
                model_func_dict={"test": "test"},
            )

    @patch(
        "hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.mlflow.artifacts.download_artifacts"  # noqa: E501
    )
    def test_mlflow_load_artifact_pkl_joblib_dict(
        self, mock_download_artifacts, mock_active_run, dummy_load_artifact
    ) -> None:
        """
        test if mlflow_load_artifact() can load a non-yaml file

        Parameters
        ----------
        mock_download_artifacts:
            mock patch mlflow.artifacts.download_artifacts
        mock_active_run:
            mock mlflow start run
        dummy_load_artifact:
            dummy load artifact dataframe
        """

        mock_active_run.return_value = MagicMock()
        mock_download_artifacts.return_value = "tests/unit_test.pkl"
        expected_return = mlflow_load_artifact(
            artifact_uri="test_uri",
            artifact_name="test",
            type_of_artifact="pkl",
        )
        pd.testing.assert_frame_equal(expected_return, dummy_load_artifact)

    @patch(
        "hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.mlflow.artifacts.download_artifacts"  # noqa: E501
    )
    def test_mlflow_load_artifact_yaml(
        self, mock_download_artifacts, mock_active_run, dummy_load_artifact
    ) -> None:
        """
        test if mlflow_load_artifact() can load a yaml file

        Parameters
        ----------
        mock_download_artifacts:
            mock patch mlflow.artifacts.download_artifacts
        mock_active_run:
            mock mlflow start run
        dummy_load_artifact:
            dummy load artifact dataframe
        """

        mock_active_run.return_value = MagicMock()
        mock_download_artifacts.return_value = (
            "tests/hip_data_ml_utils/core/test_yaml.yaml"
        )
        expected_return = mlflow_load_artifact(
            artifact_uri="test_uri",
            artifact_name="test",
            type_of_artifact="yaml",
        )
        assert isinstance(expected_return, dict)  # noqa: S101

    def test_mlflow_load_artifact_error(self) -> None:
        """
        function test for mlflow_load_artifact to raise an error
        """

        with pytest.raises(ValueError, match="Artifact type not supported"):
            mlflow_load_artifact(
                artifact_uri="test", artifact_name="test", type_of_artifact="test"
            )

    @patch("hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.mlflow.get_run")
    def test_mlflow_get_model_metrics_dict(
        self, mock_mlflow_get_run, dummy_nested_double_callable_object
    ) -> None:
        """
        test if mlflow_get_model_metrics can run correctly for dict return

        Parameters
        ----------
        mock_mlflow_get_run:
            mock patch mlflow get run function
        dummy_nested_double_callable_object:
            dummy nested callable object
        """

        mock_mlflow_get_run.return_value = dummy_nested_double_callable_object
        expected_return = mlflow_get_model_metrics(run_id="test")
        assert expected_return == {"test": 1.0}  # noqa: S101

    @patch("hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.mlflow.get_run")
    def test_mlflow_get_model_metrics_float(
        self, mock_mlflow_get_run, dummy_nested_double_callable_object
    ) -> None:
        """
        test if mlflow_get_model_metrics can run correctly for float/int return

        Parameters
        ----------
        mock_mlflow_get_run:
            mock patch mlflow get run function
        dummy_nested_double_callable_object:
            dummy nested double callable object
        """

        mock_mlflow_get_run.return_value = dummy_nested_double_callable_object
        expected_return = mlflow_get_model_metrics(
            run_id="test", key_value_metrics="test"
        )
        assert expected_return == 1.0  # noqa: S101

    def test_mlflow_get_both_registered_model_info_run_id_error(self) -> None:
        """
        function test for mlflow_get_both_registered_model_info_run_id
        """

        with pytest.raises(ValueError, match="stage can only be Staging or Production"):
            mlflow_get_both_registered_model_info_run_id(
                name="test", mlflow_client=MagicMock(), stage="test"
            )

    def test_mlflow_get_both_registered_model_info_run_id(
        self, dummy_nested_callable_object
    ) -> None:
        """
        test if mlflow_get_run_id_of_registered_model() can run correctly

        Parameters
        ----------
        dummy_nested_callable_object:
            dummy nested callable object
        """
        mock_mlflow_client = MagicMock()
        mock_mlflow_client.search_model_versions.return_value = [
            dummy_nested_callable_object
        ]
        expected_run_id, expected_class = mlflow_get_both_registered_model_info_run_id(
            name="test",
            stage="Staging",
            mlflow_client=mock_mlflow_client,
            run_id="test_123",
        )
        assert expected_run_id == "test_123"  # noqa: S101
        assert expected_class.version == 1  # noqa: S101

    def test_mlflow_promote_model_error_env(self) -> None:
        """
        test function mlflow_promote_model raises an error for incorrect env
        """

        with pytest.raises(ValueError, match="Invalid environment"):
            mlflow_promote_model(
                name="test",
                retrained_run_id="test_123",
                retrained_metric=0.0,
                start_date="test",
                eval_date="test",
                mlflow_client=MagicMock(),
                metrics_name="MAE",
                env="test",
            )

    def test_mlflow_promote_model_error_staging(
        self, dummy_nested_callable_object
    ) -> None:
        """
        test function mlflow_promote_model raises an error for model target stage

        Parameters
        ----------
        dummy_nested_callable_object:
            dummy nested double callable object
        """
        mock_mlflow_client = MagicMock()
        mock_mlflow_client.search_model_versions.return_value = [
            dummy_nested_callable_object
        ]
        with pytest.raises(ValueError, match="Model is already in target stage"):
            mlflow_promote_model(
                name="test",
                retrained_run_id="test_123",
                retrained_metric=0.0,
                start_date="test",
                eval_date="test",
                mlflow_client=mock_mlflow_client,
                metrics_name="MAE",
                env="staging",
            )

    @patch(
        "hip_data_ml_utils.mlflow_databricks.mlflow_model_utils.get_target_stage_for_env"  # noqa: E501
    )
    def test_mlflow_promote_model(
        self, mock_target_env, dummy_nested_callable_object
    ) -> None:
        """
        test if mlflow_promote_model() can run correctly

        Parameters
        ----------
        mock_rm_info:
            mocked mlflow_get_registered_model_info
        mock_target_stage:
            mocked target stage
        mock_mlflow_client:
            mocked mlflow.tracking.MlflowClient()
        """

        mock_target_env.return_value = "test"
        mock_mlflow_client = MagicMock()
        mock_mlflow_client.search_model_versions.return_value = [
            dummy_nested_callable_object
        ]

        expected_return = mlflow_promote_model(
            name="test",
            retrained_run_id="test_123",
            retrained_metric=0.0,
            start_date="test",
            eval_date="test",
            env="Staging",
            prev_run_id="test_123",
            metrics_name="MAE",
            prev_metric=0.0,
            mlflow_client=mock_mlflow_client,
        )

        assert (  # noqa: S101
            expected_return
            == "model is transitioned, and registered model description updated"
        )
