import datetime
import importlib
from typing import Callable
from typing import Dict
from typing import List

import yaml


def load_yaml(path: str) -> Dict:
    """
    function that loads the settings from the yaml file

    Parameters
    ----------
    path: str
        path to the yaml file

    Returns
    -------
    Dict
        returns a dictionary with the settings
    """
    with open(path) as f:
        settings = yaml.safe_load(f)
    return settings


def get_test_date(datetime_provided: datetime.datetime, days_difference: int) -> int:
    """
    function that returns a lookback date from specified days ago

    Parameters
    ----------
    datetime_provided: datetime.datetime
        datetime input, most likely datetime.datetime.now()
    days_difference: int
        number days ago we should look back

    Returns
    -------
    int
        returns a date dim key, yyyyMMdd
    """
    return int(
        (datetime_provided - datetime.timedelta(days=days_difference)).strftime(
            "%Y%m%d"
        )
    )


def get_function_to_load(function_dict: Dict, file_format: str) -> Callable:
    """
    function that retrieves the library function callable

    Parameters
    ----------
    function_dict: Dict
        dictionary that contains the function mapping
    file_format: str
        name of file format, pkl, parquet or delta table

    Returns
    -------
    Callable
        function that we intend to use
    """
    return getattr(
        importlib.import_module(function_dict[file_format][0]),
        function_dict[file_format][1],
    )


def get_target_stage_for_env(env: str) -> str:
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

    return "Staging" if env.lower() in {"dev", "staging"} else "Production"


def get_date_intervals_model_drift(
    date_int: int,
) -> List:
    """
    function to list of date intervals for model drift

    Parameters
    ----------
    date_int: int
        start date of monitoring in YYYYmmdd

    Returns
    -------
    List
        list of date intervals for model drift monitoring
    """
    return_list = []
    for i in range(1, 5):
        return_list.append(f"{date_int}_hour_pair_{i}")

    return return_list
