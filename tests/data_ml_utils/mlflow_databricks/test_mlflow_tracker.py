import os
import tempfile
from shutil import rmtree
from unittest.mock import MagicMock
from unittest.mock import patch

import mlflow
import pytest
from mlflow.exceptions import MlflowException

from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_artifact
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_metric
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_params
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_register_model


class TestMlflowTracking:
    """
    test class for mlflow tracking
    """

    @pytest.mark.integration
    def test_mlflow_log_artifact(self) -> None:
        """
        test if mlflow_log_artifact() can log artifact
        """

        # create a temporary artifact
        tmp_dir = tempfile.mkdtemp()
        _, path = tempfile.mkstemp(dir=tmp_dir, text=True)

        # insert text into artifact
        expected_str = "test"
        with open(path, "w") as f:
            f.write(expected_str)

        with mlflow.start_run() as run:
            expected_result = mlflow_log_artifact("test", "test", local_path=path)
            artifact_uri = run.info.artifact_uri
            artifact = mlflow.artifacts.download_artifacts(
                f"{artifact_uri}/{path[path.rfind('/')+1:]}"
            )
            with open(artifact) as f:
                artifact_content = f.read()
            assert artifact_content == expected_str  # noqa: S101
            assert expected_result == "artifact test logged"  # noqa: S101

        if os.path.exists(tmp_dir):
            rmtree(tmp_dir)

    def test_mlflow_log_artifact_error(self) -> None:
        """
        test if mlflow_log_artifact() raises the right exception
        """

        with pytest.raises(MlflowException, match="No active run to log artifact"):
            mlflow_log_artifact(artifact="test", artifact_name="test")

    @patch("data_ml_utils.mlflow_databricks.mlflow_tracker.getattr")
    def test_mlflow_log_register_model(self, mock_model_func, mock_active_run) -> None:
        """
        test if mlflow_log_model() can log model

        Parameters
        ----------
        mock_model_func:
            mock model_func
        """

        mock_active_run.return_value = MagicMock()
        mock_model_func.return_value = MagicMock()
        expected_result = mlflow_log_register_model(
            model="test",
            type_of_model="test",
            model_func_dict={"test": ["test", "test"]},
            artifact_path="test",
        )
        mock_model_func.assert_called_once()
        assert expected_result == "model logged"  # noqa: S101

    def test_mlflow_log_model_error(self) -> None:
        """
        test if mlflow_log_model() raises the right exception
        """

        with pytest.raises(ValueError, match="Model type not supported"):
            mlflow_log_register_model(
                model="test",
                type_of_model="test",
                model_func_dict={"not_test": ["not_test", "not_test"]},
                artifact_path="test",
            )

    @pytest.mark.integartion
    def test_mlflow_log_params(self) -> None:
        """
        test if mlflow_log_params() can log params
        """

        expected_params = {
            "param_1": "1",
            "param_2": "2",
            "param_3": "3",
        }

        with mlflow.start_run() as run:
            expected_result = mlflow_log_params(params=expected_params)

            logged_params_run = mlflow.get_run(run.info.run_id)

            assert len(logged_params_run.data.params) == 3  # noqa: S101
            assert logged_params_run.data.params == expected_params  # noqa: S101
            assert expected_result == f"params {expected_params} logged"  # noqa: S101

    def test_mlflow_log_params_error(self) -> None:
        """
        test if mlflow_log_params() raises the right exception
        """

        with pytest.raises(MlflowException, match="No active run to log params"):
            mlflow_log_params(params={"test": "test"})

    @pytest.mark.integartion
    def test_mlflow_log_metric(self) -> None:
        """
        test if mlflow_log_metric() can log metric
        """

        expected_metrics = {
            "metric_1": 1.0,
            "metric_2": 2.0,
            "metric_3": 3.0,
        }

        with mlflow.start_run() as run:
            expected_result_1 = mlflow_log_metric(key="metric_1", value=1.0)
            expected_result_2 = mlflow_log_metric(key="metric_2", value=2.0)
            expected_result_3 = mlflow_log_metric(key="metric_3", value=3.0)

            assert (  # noqa: S101
                expected_result_1 == "model evaluation metric metric_1, 1.0 logged"
            )
            assert (  # noqa: S101
                expected_result_2 == "model evaluation metric metric_2, 2.0 logged"
            )
            assert (  # noqa: S101
                expected_result_3 == "model evaluation metric metric_3, 3.0 logged"
            )

            logged_metric_run = mlflow.get_run(run.info.run_id)
            assert len(logged_metric_run.data.metrics) == 3  # noqa: S101

            for k, v in logged_metric_run.data.metrics.items():
                assert expected_metrics[k] == v  # noqa: S101

    def test_mlflow_log_metric_error(self) -> None:
        """
        test if mlflow_log_metric() raises the right exception
        """

        with pytest.raises(MlflowException, match="No active run to log metric"):
            mlflow_log_metric(key="test", value=1.0)
