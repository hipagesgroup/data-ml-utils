import polling
import pytest
import requests
import responses

from hip_data_ml_utils.mlflow_databricks.mlflow_serve import enable_endpoint
from hip_data_ml_utils.mlflow_databricks.mlflow_serve import get_endpoint_state_status
from hip_data_ml_utils.mlflow_databricks.mlflow_serve import get_endpoint_status
from hip_data_ml_utils.mlflow_databricks.mlflow_serve import update_compute_config


class TestServe:
    "test class for serve step"

    @responses.activate
    def test_enable_endpoint(self, dummy_url, request_time_out: int = 30) -> None:
        "test if enable_endpoint() runs correctly"

        responses.add(
            method=responses.POST,
            url=f"{dummy_url}/test_api_url",
            json={"registered_model_name": "test_model"},
            status=200,
        )
        r = requests.post(f"{dummy_url}/test_api_url", timeout=request_time_out)

        enable_endpoint_response = enable_endpoint(  # noqa: S106
            databricks_api_url="test_api_url",
            model_name="test_model",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="test_token",
        )

        assert r.json()["registered_model_name"] == "test_model"  # noqa: S101
        assert enable_endpoint_response  # noqa: S101

    @responses.activate
    def test_enable_endpoint_error(self, dummy_url, request_time_out: int = 30) -> None:
        "test if enable_endpoint() runs correctly"

        responses.add(
            method=responses.POST,
            url=f"{dummy_url}/test_api_url",
            json={"registered_model_name": "test_model"},
            status=404,
        )
        r = requests.post(f"{dummy_url}/test_api_url", timeout=request_time_out)

        with pytest.raises(requests.exceptions.HTTPError):
            enable_endpoint_response = enable_endpoint(  # noqa: S106
                databricks_api_url="test_api_url",
                model_name="test_model",
                databricks_cluster_hostname=dummy_url,
                databricks_workspace_token="test_token",
            )

            assert r.status_code == 404  # noqa: S101
            assert not enable_endpoint_response  # noqa: S101

    def test_get_endpoint_state_status(self, dummy_response) -> None:
        """
        test function for get endpoint state status

        Parameters
        ----------
        dummy_response
            a json response of a status 200 code

        Returns
        -------
        assert
            returns True that the state matches what we are expecting
        """

        assert (  # noqa: S101
            get_endpoint_state_status(dummy_response) == "ENDPOINT_STATE_READY"
        )

    def test_get_endpoint_state_status_error(self, dummy_response_error) -> None:
        """
        test function for get endpoint state status

        Parameters
        ----------
        dummy_response_error
            a json response that does not have the `state` key

        Returns
        -------
        assert
            returns True that the state matches what we are expecting
        """

        assert (  # noqa: S101
            get_endpoint_state_status(dummy_response_error) == "NOT_READY"
        )

    @responses.activate
    def test_get_endpoint_status(
        self, dummy_url, dummy_response, request_time_out: int = 30
    ) -> None:
        """
        test if get_endpoint_status() runs correctly

        Parameters
        ----------
        dummy_url
            dummy url of api
        dummy_response
            a json response of a status 200 code

        Returns
        -------
        assert
            returns True that the registered model name matches
            returns True of the get endpoint status function
        """

        responses.add(
            method=responses.GET,
            url=f"{dummy_url}/test_api_url",
            json=dummy_response,
            status=200,
        )
        r = requests.get(f"{dummy_url}/test_api_url", timeout=request_time_out)

        get_endpoint_status_response = get_endpoint_status(  # noqa: S106
            databricks_api_url="test_api_url",
            model_name="test_model",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="test_token",
            polling_step=1,
            polling_max_tries=1,
        )
        assert (  # noqa: S101
            r.json()["endpoint_status"]["registered_model_name"] == "clefairy"
        )
        assert get_endpoint_status_response  # noqa: S101

    @responses.activate
    def test_get_endpoint_status_error(
        self, dummy_url, dummy_response_error, request_time_out: int = 30
    ) -> None:
        """
        test if get_endpoint_status() runs correctly

        Parameters
        ----------
        dummy_url
            dummy url of api
        dummy_response_error
            a json response that does not have the `state` key

        Returns
        -------
        assert
            returns assertion of registered model name matches
            returns False of the get endpoint status function
        """
        responses.add(
            method=responses.GET,
            url=f"{dummy_url}/test_api_url",
            json=dummy_response_error,
            status=404,
        )
        r = requests.get(f"{dummy_url}/test_api_url", timeout=request_time_out)

        with pytest.raises(polling.MaxCallException):
            get_endpoint_status_response = get_endpoint_status(  # noqa: S106
                databricks_api_url="test_api_url",
                model_name="test_model",
                databricks_cluster_hostname=dummy_url,
                databricks_workspace_token="test_token",
                polling_step=1,
                polling_max_tries=1,
            )
            assert (  # noqa: S101
                r.json()["endpoint_status"]["registered_model_name"] == "clefairy"
            )
            assert not get_endpoint_status_response  # noqa: S101

    @responses.activate
    def test_update_compute_config(self, dummy_url, request_time_out: int = 30) -> None:
        "test if update_compute_config() runs correctly"

        responses.add(
            method=responses.PUT,
            url=f"{dummy_url}/test_api_url",
            json={
                "registered_model_name": "test_model",
                "stage": "test_stage",
                "desired_workload_config_spec": {
                    "workload_size_id": "test",
                    "scale_to_zero_enabled": "test",
                },
            },
            status=200,
        )
        r = requests.put(f"{dummy_url}/test_api_url", timeout=request_time_out)

        update_compute_config_response = update_compute_config(  # noqa: S106
            databricks_api_url="test_api_url",
            model_name="test_model",
            stage="test_stage",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="test_token",
            workload_size_id="test_workload_size_id",
            scale_to_zero_enabled="test_scale_to_zero_enabled",
        )

        assert r.json()["registered_model_name"] == "test_model"  # noqa: S101
        assert r.json()["stage"] == "test_stage"  # noqa: S101
        assert (  # noqa: S101
            r.json()["desired_workload_config_spec"]["workload_size_id"] == "test"
        )
        assert update_compute_config_response == 0  # noqa: S101

    @responses.activate
    def test_update_compute_config_error(
        self, dummy_url, request_time_out: int = 30
    ) -> None:
        "test if update_compute_config() runs correctly"

        responses.add(
            method=responses.PUT,
            url=f"{dummy_url}/test_api_url",
            json={
                "registered_model_name": "test_model",
                "stage": "test_stage",
                "desired_workload_config_spec": {
                    "workload_size_id": "test",
                    "scale_to_zero_enabled": "test",
                },
            },
            status=404,
        )
        r = requests.put(f"{dummy_url}/test_api_url", timeout=request_time_out)

        update_compute_config_response = update_compute_config(  # noqa: S106
            databricks_api_url="test_api_url",
            model_name="test_model",
            stage="test_stage",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="test_token",
            workload_size_id="test_workload_size_id",
            scale_to_zero_enabled="test_scale_to_zero_enabled",
        )
        assert r.json()["registered_model_name"] == "test_model"  # noqa: S101
        assert update_compute_config_response == 1  # noqa: S101
