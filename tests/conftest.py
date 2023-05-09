import os
from unittest.mock import patch

import pandas as pd
import pytest


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # pragma: allowlist secret
    os.environ[  # pragma: allowlist secret
        "AWS_SECRET_ACCESS_KEY"  # noqa: S105
    ] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"  # pragma: allowlist secret
    os.environ["S3_BUCKET"] = "s3://au-com-dummy/athena_queries/"


@pytest.fixture
def mock_active_run():
    """mocked mlflow.active_run()"""

    with patch(
        "hip_data_ml_utils.mlflow_databricks.mlflow_tracker.mlflow.active_run"
    ) as mock_active_run:
        mock_active_run.return_value = None
        yield mock_active_run


@pytest.fixture(autouse=True)
def dummy_function_dict():
    return {"parquet": ["awswrangler.s3", "read_parquet"], "pkl": ["joblib", "load"]}


@pytest.fixture(autouse=True)
def dummy_test_table():
    return "dev.test_table"


@pytest.fixture(autouse=True)
def dummy_load_artifact():
    return pd.DataFrame(
        {
            "season": "winter",
        },
        index=[0],
    )


@pytest.fixture(autouse=True)
def dummy_nested_double_callable_object():
    class first_class:
        def __init__(self):
            self.return_value = second_class()

        @property
        def data(self):
            return self.return_value

    class second_class:
        @property
        def metrics(self):
            return {"test": 1.0}

    return first_class()


@pytest.fixture(autouse=True)
def dummy_nested_callable_object():
    class first_class:
        def __init__(self):
            self.current_stage = self.current_stage()
            self.run_id = self.run_id()
            self.version = self.version()

        def current_stage(self):
            return "Staging"

        def run_id(self):
            return "test_123"

        def version(self):
            return 1

    return first_class()


@pytest.fixture(autouse=True)
def dummy_response():
    return {
        "state": {
            "ready": "READY",
            "config_update": "IN_PROGRESS",
        }
    }


@pytest.fixture(autouse=True)
def dummy_response_error():
    return {
        "endpoint_status": {
            "registered_model_name": "clefairy",
            "state_message": "Waiting for deployment to be created.",
        }
    }


@pytest.fixture(scope="module")
def dummy_url():
    """dummy url"""

    return "https://test.com"


@pytest.fixture(autouse=True)
def dummy_json_response():
    return {
        "predictions": {
            "data": [
                {
                    "practice_id": 394,
                    "practice_parent_id": 55,
                    "practice_seo_key": "handyman_basic_painting",
                    "practice_seo_name": "Basic Painting",
                    "practice_parent_seo_name": "Handyman",
                    "practice_parent_seo_key": "Handyman",
                    "ranking": 0.3340230470456127,
                }
            ]
        }
    }


@pytest.fixture(autouse=True)
def dummy_settings_error():
    return {
        "random": {
            "top_result": {"parent_seo_name": "Not related"},
            "keywords": "random",
        }
    }


@pytest.fixture(autouse=True)
def dummy_settings_success():
    return {
        "random": {
            "top_result": {"parent_seo_name": "Basic Painting"},
            "keywords": "random",
        }
    }
