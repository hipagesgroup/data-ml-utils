import os
from unittest.mock import patch

import pytest


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # pragma: allowlist secret
    os.environ[  # pragma: allowlist secret
        "AWS_SECRET_ACCESS_KEY"  # noqa: S105
    ] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"  # pragma: allowlist secret


@pytest.fixture
def mock_active_run():
    """mocked mlflow.active_run()"""

    with patch(
        "data_ml_utils.mlflow_databricks.mlflow_tracker.mlflow.active_run"
    ) as mock_active_run:
        mock_active_run.return_value = None
        yield mock_active_run


@pytest.fixture(autouse=True)
def dummy_function_dict():
    return {"parquet": ["awswrangler.s3", "read_parquet"], "pkl": ["joblib", "load"]}
