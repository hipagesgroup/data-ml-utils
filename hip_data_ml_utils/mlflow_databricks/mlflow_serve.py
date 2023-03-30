import logging

import polling
import requests

log = logging.getLogger(__name__)


def enable_endpoint(
    databricks_api_url: str,
    model_name: str,
    databricks_cluster_hostname: str,
    databricks_workspace_token: str,
    request_time_out: int = 60,
) -> bool:
    """
    function to enable the endpoint of a registered model

    Parameters
    ----------
    databricks_api_url: str
        url of the databricks api
    model_name: str
        name of the registered model
    databricks_cluster_hostname: str
        hostname of the databricks cluster
    databricks_workspace_token: str
        token of the databricks workspace
    request_time_out: int
        timeout for the request

    Returns
    -------
    bool
        True if the endpoint was enabled successfully
        raise an exception otherwise
    """

    url = f"{databricks_cluster_hostname}/{databricks_api_url}"
    headers = {"Authorization": f"Bearer {databricks_workspace_token}"}
    json = {"registered_model_name": model_name}

    response = requests.post(
        url=url,
        headers=headers,
        json=json,
        timeout=request_time_out,
    )
    if response.status_code != 200:
        response.raise_for_status()

    return True


def get_endpoint_state_status(response_json: dict) -> str:
    """
    function that returns endpoint state

    Parameters
    ----------
    response_json: Dict
        json response of the get request of mlflow get-status

    Returns
    -------
    str
        returns the state of the endpoint
    """
    try:
        return response_json["endpoint_status"]["state"]
    except Exception:
        return "NOT_READY"


def get_endpoint_status(
    databricks_api_url: str,
    model_name: str,
    databricks_cluster_hostname: str,
    databricks_workspace_token: str,
    polling_step: int = 10,
    polling_max_tries: int = 42,
    request_time_out: int = 60,
) -> bool:
    """
    function to get the status of the endpoint

    Parameters
    ----------
    databricks_api_url: str
        url of the databricks api
    model_name: str
        name of the registered model
    databricks_cluster_hostname: str
        hostname of the databricks cluster
    databricks_workspace_token: str
        token of the databricks workspace
    polling_step: int
        step size for polling
    polling_max_tries: int
        maximum number of tries for polling
    request_time_out: int
        timeout for the request

    Returns
    -------
    bool
        True if the endpoint is ready
        raise an exception otherwise
    """

    url = f"{databricks_cluster_hostname}/{databricks_api_url}"
    headers = {"Authorization": f"Bearer {databricks_workspace_token}"}
    json = {"registered_model_name": model_name}

    polling_response = polling.poll(
        lambda: get_endpoint_state_status(
            requests.get(
                url=url,
                headers=headers,
                json=json,
                timeout=request_time_out,
            ).json()
        )
        == "ENDPOINT_STATE_READY",
        step=polling_step,
        ignore_exceptions=(requests.exceptions.ConnectionError,),
        poll_forever=False,
        max_tries=polling_max_tries,
    )

    if not polling_response:
        polling_response.raise_for_status()

    return True


def update_compute_config(
    databricks_api_url: str,
    model_name: str,
    stage: str,
    databricks_cluster_hostname: str,
    databricks_workspace_token: str,
    workload_size_id: str,
    scale_to_zero_enabled: str,
    request_time_out: int = 60,
) -> int:
    """
    function to scale the endpoint to zero

    Parameters
    ----------
    databricks_api_url: str
        url of the databricks api
    model_name: str
        name of the registered model
    stage: str
        stage of the registered model (e.g. Staging or Production)
    databricks_cluster_hostname: str
        hostname of the databricks cluster
    databricks_workspace_token: str
        token of the databricks workspace
    workload_size_id: str
        workload size id of the endpoint (e.g. Small, Medium, Large)
    scale_to_zero_enabled: str
        flag to enable/disable scaling to zero
        "true" to enable scaling to zero
        "false" to disable scaling to zero
    request_time_out: int
        timeout for the request

    Returns
    -------
    int
        0 if the compute config is updated successfully, 1 otherwise
    """
    url = f"{databricks_cluster_hostname}/{databricks_api_url}"
    headers = {"Authorization": f"Bearer {databricks_workspace_token}"}
    json = {
        "registered_model_name": model_name,
        "stage": stage.capitalize(),
        "desired_workload_config_spec": {
            "workload_size_id": f"{workload_size_id.capitalize()}",
            "scale_to_zero_enabled": f"{scale_to_zero_enabled}",
        },
    }

    compute_config_response = requests.put(
        url=url,
        headers=headers,
        json=json,
        timeout=request_time_out,
    )

    if compute_config_response.status_code != 200:
        log.warning(
            f"""status_code: {compute_config_response.status_code}, """
            f"""json_response: {compute_config_response.json()}"""
        )
        return 1

    return 0
