import json
import logging

import requests

log = logging.getLogger(__name__)


def verify_prediction(response_json: dict, expected_keywords_response: str) -> bool:
    """
    function that returns endpoint state

    Parameters
    ----------
    response_json: dict
        json response of the post request from model endpoint
    keywords_response: str
        expected top parent seo name for keywords

    Returns
    -------
    int
        non exit response if response matches
    """
    response_from_clefairy = response_json["predictions"]["data"][0][
        "practice_seo_name"
    ]
    return response_from_clefairy in expected_keywords_response


def get_requests(
    model_name: str,
    databricks_cluster_hostname: str,
    databricks_workspace_token: str,
    settings: dict,
    keywords: str,
    request_time_out: int = 60,
) -> int:
    """
    function to validate response from model endpoint

    Parameters
    ----------
    model_name: str
        name of the registered model
    databricks_cluster_hostname: str
        hostname of the databricks cluster
    databricks_workspace_token: str
        token of the databricks workspace
    settings: dict
        repo settings and configuration
    keywords: str
        keywords to be used for prediction
    request_time_out: int
        time out for the request

    Returns
    -------
    bool
        True if the endpoint was enabled successfully
        raise an exception otherwise
    """

    url = (
        f"""{databricks_cluster_hostname}/serving-endpoints/"""
        f"""{model_name}/invocations"""
    )
    headers = {
        "Authorization": f"Bearer {databricks_workspace_token}",
        "Content-Type": "application/json",
    }

    data_json = {
        "dataframe_split": {
            "index": [0],
            "columns": ["keywords", "session_id", "device_token"],
            "data": [[settings[keywords]["keywords"], "test", "test"]],
        }
    }

    # make post request
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data_json),
        timeout=request_time_out,
    )

    if response.status_code != 200:
        log.warning(
            """model endpoint response has errors, """
            f"""{response.status_code}, {response.json()}"""
        )
        return 1

    # verify prediction
    if not verify_prediction(
        response.json(), settings[keywords]["top_result"]["parent_seo_name"]
    ):
        log.warning(f"{keywords} keywords mismatch, pls check model")
        return 1

    return 0
