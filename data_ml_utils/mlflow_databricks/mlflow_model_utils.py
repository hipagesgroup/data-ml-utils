from typing import Any
from typing import Dict

import mlflow
import pandas as pd
from joblib import load
from mlflow.tracking import MlflowClient
from steps.evaluate import get_mae_rmse_metrics


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
    else:
        raise ValueError("Model type not supported")


def mlflow_load_artifact(
    artifact_uri: str,
    artifact_name: str,
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

    return load(
        mlflow.artifacts.download_artifacts(
            artifact_uri=f"{artifact_uri}/{artifact_name}"
        )
    )


def mlflow_register_model(model_uri: str, name: str) -> None:
    """
    function to register model to mlflow model registry
    Parameters
    ----------
    model_uri: str
        uri of the model to be registered
    name: str
        name of the model to be registered
    """

    mlflow.register_model(model_uri=model_uri, name=name)


def mlflow_get_run_id_of_registered_model(name: str, stage: str = "Production") -> str:
    """
    function to get run_id of registered model given its stage

    Parameters
    ----------
    name: str
        name of registered model
    stage: str
        stage of registered model
        can only be "Staging" or "Production"
    """

    if stage not in ["Staging", "Production"]:
        raise ValueError("stage can only be Staging or Production")

    for _, rm in enumerate(MlflowClient().search_model_versions(f"name='{name}'")):
        if rm.current_stage == stage:
            return rm.run_id


def mlflow_get_registered_model_info(name: str, run_id: str) -> dict:
    """
    function to get registered model info

    Parameters
    ----------
    name: str
        name of registered model
    run_id: str
        run_id of registered model
    """

    for _, rm in enumerate(MlflowClient().search_model_versions(f"name='{name}'")):
        if rm.run_id == run_id:
            return rm


def mlflow_get_target_stage_for_env(env: str) -> str:
    """
    function to get corresponding target stage based on running environment

    Parameters
    ----------
    env: str
        running environment "dev", "staging" or "prod"

    Returns
    -------
    str
        target stage
        "Staging" for "dev" and "staging" env
        "Production" for "prod" env
    """

    if not (isinstance(env, str)) or (env.lower() not in ["dev", "staging", "prod"]):
        raise ValueError("Invalid environment")

    return "Staging" if env.lower() in ("dev", "staging") else "Production"


def mlflow_promote_model(
    name: str,
    retrained_run_id: str,
    retrained_metric: float,
    eval_date: str,
    env: str,
    prev_run_id: str = None,
    prev_metric: float = 0.0,
) -> None:
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
    eval_date: str
        evaluation data date
        from beginning to eval_date
    env: str
        running environment "dev", "staging" or "prod"
    prev_run_id: str
        default None, run_id of previous model
    prev_metric: float
        default 0.0, metric of previous model
    """

    if not (isinstance(env, str)) or (env.lower() not in ["dev", "staging", "prod"]):
        raise ValueError("Invalid environment")

    target_stage = mlflow_get_target_stage_for_env(env)
    rm_retrained = mlflow_get_registered_model_info(name=name, run_id=retrained_run_id)

    if rm_retrained.current_stage != target_stage:
        client = MlflowClient()
        client.transition_model_version_stage(
            name=name,
            version=rm_retrained.version,
            stage=target_stage,
            archive_existing_versions=True,
        )

        prev_version = ""
        if prev_run_id:
            prev_version = mlflow_get_registered_model_info(
                name=name, run_id=prev_run_id
            ).version

        client.update_model_version(
            name=name,
            version=rm_retrained.version,
            description=f"""
            Data                        : 2021-02-01 to {eval_date}
            Curr Version                : {rm_retrained.version}
            Curr Overall MAE            : {retrained_metric:.4f}
            Prev Version                : {prev_version}
            Prev Overall MAE            : {prev_metric:.4f}
            """,
        )
    else:
        raise ValueError("Model is already in target stage")


def mlflow_decision_to_promote(
    mlflow_model_name: str,  # NOSONAR
    artifact_path: str,
    type_of_model: str,
    model_func_dict: dict,
    env: str,
    X_test: pd.DataFrame,  # NOSONAR
    y_test: pd.DataFrame,
    retrained_run_id: str,
    eval_date: str,
    target_name: str,
    predict_name: str,
    metrics_dict: Dict,
) -> None:
    """
    function to decide whether to register/promote model based on the current env

    Parameters
    ----------
    mlflow_model_name: str
        model name registered in mlflow
    artifact_path: str
        the directory in ``artifact_uri`` to write to
    type_of_model: str
        type of model
    model_func_dict: dict
        dictionary of model function to call
    pyfunc_model_path: str
        path to pyfunc model
    env: str
        running environment "dev", "staging" or "prod"
    top_n: int
        top n predictions to evaluate
    X: np.ndarray
        feature array
    y: np.ndarray
        target array
    df: pd.DataFrame
        features + parent_cat_col + target
    max_performance_drop_by_parent_cat: float
        0.0 <= max_performance_drop_by_parent_cat <= 1.0
        represents the maximum acceptable performance drop
    retrained_run_id: str
        run_id of the retrained model
    eval_date: str
        evaluation data date
        from beginning to eval_date
    """

    # get run_id of existing model in production
    current_model_run_id = mlflow_get_run_id_of_registered_model(
        name=mlflow_model_name,
        stage=mlflow_get_target_stage_for_env(env=env),
    )

    if (current_model_run_id is not None) and (env == "prod"):
        current_model = mlflow_load_model(
            model_uri=f"runs:/{current_model_run_id}/{artifact_path}",
            type_of_model=type_of_model,
            model_func_dict=model_func_dict,
        )

        _, _, _, metrics_dict_current = get_mae_rmse_metrics(
            model=current_model,
            X_test=X_test,
            y_test=y_test,
            target_name=target_name,
            predict_name=predict_name,
            mlflow_logging=False,
        )

        if metrics_dict_current["mae_overall"] >= metrics_dict["mae_overall"]:
            mlflow_promote_model(
                name=mlflow_model_name,
                retrained_run_id=retrained_run_id,
                retrained_metric=metrics_dict["mae_overall"],
                eval_date=eval_date,
                env=env,
                prev_run_id=current_model_run_id,
                prev_metric=metrics_dict_current["mae_overall"],
            )
    else:
        mlflow_promote_model(
            name=mlflow_model_name,
            retrained_run_id=retrained_run_id,
            retrained_metric=metrics_dict["mae_overall"],
            eval_date=eval_date,
            env=env,
        )
