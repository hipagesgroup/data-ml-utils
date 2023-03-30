import requests
import responses

from data_ml_utils.mlflow_databricks.mlflow_prediction_requests import get_requests
from data_ml_utils.mlflow_databricks.mlflow_prediction_requests import verify_prediction


class TestPredictionRequests:
    "test class for prediction requests"

    def test_verify_prediction(self, dummy_json_response) -> None:
        """
        test function for verify prediction

        Parameters
        ----------
        dummy_json_response
            dummy json response of a successful prediction

        Returns
        -------
        assert
            returns True that the prediction matches
        """
        expected_result = True
        expected_mismatch = False
        assert (  # noqa: S101
            verify_prediction(dummy_json_response, "Basic Painting") == expected_result
        )
        assert (  # noqa: S101
            verify_prediction(dummy_json_response, "Ikea Kitchen") == expected_mismatch
        )

    @responses.activate
    def test_get_requests_error(
        self, dummy_url, dummy_json_response, request_time_out: int = 30
    ) -> None:
        """
        test function for get requests to have error requests from model endpoint

        Parameters
        ----------
        dummy_url
            dummy url for post requests
        dummy_json_response
            dummy json response of a successful prediction

        Returns
        -------
        assert
            returns exit value function
        """

        responses.add(
            method=responses.POST,
            url=f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            json=dummy_json_response,
            status=400,
        )

        r = requests.post(
            f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            timeout=request_time_out,
        )

        model_response = get_requests(  # noqa: S106
            model_name="test_model",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="wonderful",
            settings={"random": {"keywords": "testing"}},
            keywords="random",
        )

        assert model_response == 1  # noqa: S101
        assert r.status_code != 200  # noqa: S101

    @responses.activate
    def test_get_requests_success_error_verification(
        self,
        dummy_url,
        dummy_json_response,
        dummy_settings_error,
        request_time_out: int = 30,
    ) -> None:
        """
        test function for get requests to have successful post request
        but error in verification

        Parameters
        ----------
        dummy_url
            dummy url for post requests
        dummy_json_response
            dummy json response of a successful prediction
        dummy_settings_error
            dummy error settings response for model verification

        Returns
        -------
        assert
            returns exit value function
        """

        responses.add(
            method=responses.POST,
            url=f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            json=dummy_json_response,
            status=200,
        )

        r = requests.post(
            f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            timeout=request_time_out,
        )

        model_response = get_requests(  # noqa: S106
            model_name="test_model",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="wonderful",
            settings=dummy_settings_error,
            keywords="random",
        )

        assert model_response == 1  # noqa: S101
        assert r.status_code == 200  # noqa: S101

    @responses.activate
    def test_get_requests_success(
        self,
        dummy_url,
        dummy_json_response,
        dummy_settings_success,
        request_time_out: int = 30,
    ) -> None:
        """
        test function for get requests to have successful post request

        Parameters
        ----------
        dummy_url
            dummy url for post requests
        dummy_json_response
            dummy json response of a successful prediction
        dummy_settings_success
            dummy successful settings response for model verification

        Returns
        -------
        assert
            returns non exit value function
        """

        responses.add(
            method=responses.POST,
            url=f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            json=dummy_json_response,
            status=200,
        )

        r = requests.post(
            f"{dummy_url}/model-endpoint/test_model/Production/invocations",
            timeout=request_time_out,
        )

        model_response = get_requests(  # noqa: S106
            model_name="test_model",
            databricks_cluster_hostname=dummy_url,
            databricks_workspace_token="wonderful",
            settings=dummy_settings_success,
            keywords="random",
        )

        assert model_response == 0  # noqa: S101
        assert r.status_code == 200  # noqa: S101
