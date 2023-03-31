from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union

import mlflow
from joblib import load

from hip_data_ml_utils.core.databricks_utils import get_target_stage_for_env
from hip_data_ml_utils.core.databricks_utils import load_yaml


def mlflow_load_model(
    model_uri: str,
    type_of_model: str,
    model_func_dict: dict,
) -> Any:
    """
    function to load model from mlflow

    Parameters
    ----------
    model_uri: str
        URI of the model to load
    type_of_model: str
        type of model to load
    model_func_dict: dict
        dictionary of model function to call

    Returns
    -------
    Any
        model
    """

    if type_of_model in model_func_dict:
        model_func = getattr(mlflow, model_func_dict[type_of_model][0])
        return model_func.load_model(model_uri=model_uri)

    raise ValueError("Model type not supported")


def mlflow_load_artifact(
    artifact_uri: str,
    artifact_name: str,
    type_of_artifact: str = "joblib",
) -> Any:
    """
    function to load artifact from mlflow

    Parameters
    ----------
    artifact_uri: str
        URI pointing to the artifacts, such as
        ``"runs:/500cf58bee2b40a4a82861cc31a617b1/my_model.pkl"``,
        ``"models:/my_model/Production"``, or ``"s3://my_bucket/my/file.txt"``
    artifact_name: str
        Name of the artifact to load

    Returns
    -------
    Any
        artifact
    """

    if type_of_artifact not in ("joblib", "pkl", "dict", "yaml"):
        raise ValueError("Artifact type not supported")

    if type_of_artifact in ("joblib", "pkl", "dict"):
        return load(
            mlflow.artifacts.download_artifacts(
                artifact_uri=f"{artifact_uri}/{artifact_name}"
            )
        )
    return load_yaml(
        mlflow.artifacts.download_artifacts(
            artifact_uri=f"{artifact_uri}/{artifact_name}"
        )
    )


def mlflow_get_model_metrics(
    run_id: str, key_value_metrics: str = None
) -> Union[float, int, Dict]:
    """
    function to get model evaluation metrics from mlflow run

    Parameters
    ----------
    run_id: str
        unique identifier of mlflow run
    key_value: str
        name of metrics

    Returns
    -------
    Union[float, int, Dict]
        return evaluation metric in int or float, or all metrics with Dict
    """

    model_metrics_informtion = mlflow.get_run(
        run_id=run_id,
    ).data.metrics

    if key_value_metrics is None:
        return model_metrics_informtion

    return model_metrics_informtion[key_value_metrics]


def mlflow_get_both_registered_model_info_run_id(
    name: str,
    mlflow_client: mlflow.tracking.client.MlflowClient,
    run_id: str = None,
    stage: str = "Production",
) -> Tuple[str, Dict]:
    """
    function to get run_id of registered model given its stage
    also gets registered model info

    Parameters
    ----------
    name: str
        name of registered model
    run_id: str
        unique identifier of mlflow run of registered model
    mlflow_client: mlflow.tracking.client.MlflowClient
        initialised mlflow client
    stage: str
        stage of registered model; Staging or Production

    Returns
    -------
    str
        current model mlflow run_id
    Dict
        registered model info; version, description, run_id, current_stage, etc
    """

    if stage not in ["Staging", "Production"]:
        raise ValueError("stage can only be Staging or Production")

    current_model_run_id = None
    registered_model_information = None

    for _, rm in enumerate(mlflow_client.search_model_versions(f"name='{name}'")):
        if rm.current_stage == stage:
            current_model_run_id = rm.run_id
        if rm.run_id == run_id:
            registered_model_information = rm
    return current_model_run_id, registered_model_information


def mlflow_promote_model(
    name: str,
    retrained_run_id: str,
    retrained_metric: float,
    start_date: str,
    eval_date: str,
    env: str,
    mlflow_client: mlflow.tracking.client.MlflowClient,
    metrics_name: str,
    prev_run_id: str = None,
    prev_metric: float = 0.0,
) -> str:
    """
    function to promote registered model to corresponding stage based on running env
    and then update the description of the promoted model

    Parameters
    ----------
    name: str
        name of the registered model to be promoted
    retrained_run_id: str
        run_id of the registered retrained model to be promoted
    retrained_metric: float
        metric of retrained model
    start_date: str
        start date of training data
    eval_date: str
        evaluation data date
        from beginning to eval_date
    env: str
        running environment "dev", "staging" or "prod"
    mlflow_client: mlflow.tracking.client.MlflowClient
        initialised mlflow client
    metrics_name: str
        name of primary evaluation metric captured
    prev_run_id: str
        default None, run_id of previous model
    prev_metric: float
        default 0.0, metric of previous model

    Returns
    -------
    str
        response if model being transitioned and update registered model description
    """

    target_stage = get_target_stage_for_env(env=env)
    _, rm_retrained = mlflow_get_both_registered_model_info_run_id(
        name=name,
        run_id=retrained_run_id,
        mlflow_client=mlflow_client,
    )

    if rm_retrained.current_stage != target_stage:
        mlflow_client.transition_model_version_stage(
            name=name,
            version=rm_retrained.version,
            stage=target_stage,
            archive_existing_versions=True,
        )

        prev_version = ""
        if prev_run_id:
            _, prev_run = mlflow_get_both_registered_model_info_run_id(
                name=name,
                run_id=prev_run_id,
                mlflow_client=mlflow_client,
            )
            prev_version = prev_run.version

        mlflow_client.update_model_version(
            name=name,
            version=rm_retrained.version,
            description=f"""
            Data                            : {start_date} to {eval_date}
            Curr Version                    : {rm_retrained.version}
            Curr Overall {metrics_name}     : {retrained_metric:.4f}
            Prev Version                    : {prev_version}
            Prev Overall MAE {metrics_name} : {prev_metric:.4f}
            """,
        )
        return "model is transitioned, and registered model description updated"
    raise ValueError("Model is already in target stage")
