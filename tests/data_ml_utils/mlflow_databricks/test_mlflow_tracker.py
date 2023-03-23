import os
import tempfile
from shutil import rmtree
from unittest.mock import MagicMock
from unittest.mock import patch

import mlflow
import pytest
from mlflow.exceptions import MlflowException

from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_end_run
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_artifact
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_artifacts
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_metric
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_params
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_log_register_model
from data_ml_utils.mlflow_databricks.mlflow_tracker import mlflow_start_run


class TestMlflowRun:
    """
    test class for starting and ending mlflow run
    """

    @patch("data_ml_utils.mlflow_databricks.mlflow_tracker.mlflow.start_run")
    def test_mlflow_start_run(self, mock_start_run) -> None:
        """
        test if mlflow_start_run() can run correctly

        Parameters
        ----------
        mock_start_run:
            mocked mlflow.start_run
        """

        mock_start_run.return_value = MagicMock()
        mlflow_start_run(run_name="test_run", experiment_id="test_id")
        mock_start_run.assert_called_once_with(
            run_name="test_run",
            experiment_id="test_id",
        )

    def test_mlflow_start_run_error(self, mock_active_run) -> None:
        """
        test mlflow_start_run error
        """

        with pytest.raises(MlflowException, match="Run already active"):
            mock_active_run.return_value = MagicMock()
            mlflow_start_run(run_name="test_run")

    @patch("data_ml_utils.mlflow_databricks.mlflow_tracker.mlflow.end_run")
    def test_mlflow_end_run(self, mock_end_run, mock_active_run) -> None:
        """
        test if mlflow_end_run() can end run

        Parameters
        ----------
        mock_end_run:
            mocked mlflow.end_run
        """

        mock_active_run.return_value = MagicMock()
        mock_end_run.return_value = MagicMock()
        mlflow_end_run()
        mock_end_run.assert_called_once()

    def test_mlflow_end_run_error(self) -> None:
        """
        test mlflow_end_run error
        """

        with pytest.raises(MlflowException, match="No active run to end"):
            mlflow_end_run()


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
            mlflow_log_artifact("test", "test", local_path=path)
            artifact_uri = run.info.artifact_uri
            artifact = mlflow.artifacts.download_artifacts(
                f"{artifact_uri}/{path[path.rfind('/')+1:]}"
            )
            with open(artifact) as f:
                artifact_content = f.read()
            assert artifact_content == expected_str  # noqa: S101

        if os.path.exists(tmp_dir):
            rmtree(tmp_dir)

    def test_mlflow_log_artifact_error(self) -> None:
        """
        test if mlflow_log_artifact() raises the right exception
        """

        with pytest.raises(MlflowException, match="No active run to log artifact"):
            mlflow_log_artifact(artifact="test", artifact_name="test")

    @pytest.mark.integration
    def test_mlflow_log_artifacts(self) -> None:
        """
        test if mlflow_log_artifacts() can log artifacts
        """

        # create temporary artifacts
        tmp_dir = tempfile.mkdtemp()
        _, path_0 = tempfile.mkstemp(dir=tmp_dir, text=True)
        _, path_1 = tempfile.mkstemp(dir=tmp_dir, text=True)

        # insert text into artifacts
        for i, path in enumerate([path_0, path_1]):
            expected_str = "test"
            with open(path, "w") as f:
                f.write(f"{expected_str}_{i}")

        with mlflow.start_run() as run:
            mlflow_log_artifacts(local_dir=tmp_dir)
            artifact_uri = run.info.artifact_uri

            for i, path in enumerate([path_0, path_1]):
                artifact = mlflow.artifacts.download_artifacts(
                    f"{artifact_uri}/{path[path.rfind('/')+1:]}"
                )
                with open(artifact) as f:
                    artifact_content = f.read()
                assert artifact_content == f"{expected_str}_{i}"  # noqa: S101

        if os.path.exists(tmp_dir):
            rmtree(tmp_dir)

    def test_mlflow_log_artifacts_error(self) -> None:
        """
        test if mlflow_log_artifact() raises the right exception
        """

        with pytest.raises(MlflowException, match="No active run to log artifacts"):
            mlflow_log_artifacts(local_dir="test")

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
        mlflow_log_register_model(
            model="test",
            type_of_model="test",
            model_func_dict={"test": ["test", "test"]},
            artifact_path="test",
        )
        mock_model_func.assert_called_once()

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
            mlflow_log_params(params=expected_params)

            logged_params_run = mlflow.get_run(run.info.run_id)

            assert len(logged_params_run.data.params) == 3  # noqa: S101
            assert logged_params_run.data.params == expected_params  # noqa: S101

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
            mlflow_log_metric(key="metric_1", value=1.0)
            mlflow_log_metric(key="metric_2", value=2.0)
            mlflow_log_metric(key="metric_3", value=3.0)

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
