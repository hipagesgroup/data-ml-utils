import tempfile
from typing import Any
from typing import Optional

import mlflow
from joblib import dump
from mlflow.exceptions import MlflowException


def mlflow_log_artifact(
    artifact: Any,
    artifact_name: str,
    local_path: Optional[str] = None,
    artifact_path: Optional[str] = None,
) -> str:
    """
    function to log artifact to mlflow

    Parameters
    ----------
    artifact: Any
        artifact to log
    artifact_name: str
        name of the artifact
    local_path: Optional[str]
        If provided, the local path to the artifact
    artifact_path: Optional[str]
        If provided, the directory in ``artifact_uri`` to write to
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        if local_path is None:
            local_path = f"{tmp_dir}/{artifact_name}.joblib"
            dump(artifact, local_path)

        if mlflow.active_run():
            mlflow.log_artifact(local_path=local_path, artifact_path=artifact_path)
            return f"artifact {artifact_name} logged"

        raise MlflowException("No active run to log artifact")


def mlflow_log_register_model(
    model,
    type_of_model: str,
    model_func_dict: dict,
    artifact_path: str,
    name_of_registered_model: str = None,
    extra_pip_requirements: Optional[list] = None,
    code_path: Optional[list] = None,
) -> str:
    """
    function to log and register model to mlflow

    Parameters
    ----------
    model: object
        model object
    type_of_model: str
        type of model to log
    model_func_dict: dict
        dictionary of model function to call
    artifact_path: str
        Run-relative artifact path
    name_of_registered_model: str
        name of registered model, if it does not exist it will register a new model
        if it does, it will register a new version to the model
        does not register if it is None
    extra_pip_requirements: Optional[list] = None
        Either an iterable of pip requirement strings
            (e.g. ["pandas", "-r requirements.txt", "-c constraints.txt"])
        or the string path to a pip requirements file on the local filesystem
            (e.g. "requirements.txt").
        If provided, this describes additional pip requirements that are appended
        to a default set of pip requirements generated automatically based on
        the user’s current software environment. Both requirements and
        constraints are automatically parsed and written to requirements.txt
        and constraints.txt files, respectively, and stored as part of the model.
        Requirements are also written to the pip section of the model’s conda
        environment (conda.yaml) file.
    code_path: Optional[list] = None
        A list of local filesystem paths to Python file dependencies
        (or directories containing file dependencies).
        These files are prepended to the system path before
        the model is loaded.
    """

    if type_of_model in model_func_dict:
        if mlflow.active_run():
            model_func = getattr(mlflow, model_func_dict[type_of_model][0])
            model_func.log_model(
                **{type_of_model: model, model_func_dict[type_of_model][1]: code_path},
                registered_model_name=name_of_registered_model,
                artifact_path=artifact_path,
                extra_pip_requirements=extra_pip_requirements,
            )
            return (
                "model logged"
                if name_of_registered_model is None
                else f"model logged and registered as {name_of_registered_model}"
            )

        raise MlflowException("No active run to log model")

    raise ValueError("Model type not supported")


def mlflow_log_params(params: dict) -> str:
    """
    function to log params to mlflow

    Parameters
    ----------
    params: dict
        dictionary of params
    """

    if mlflow.active_run():
        mlflow.log_params(params=params)
        return f"params {params} logged"

    raise MlflowException("No active run to log params")


def mlflow_log_metric(key: str, value: float) -> str:
    """
    function to log metric to mlflow

    Parameters
    ----------
    key: str
        metric name
    value: float
        metric value
    """

    if mlflow.active_run():
        mlflow.log_metric(key=key, value=value)
        return f"model evaluation metric {key}, {value} logged"

    raise MlflowException("No active run to log metric")
