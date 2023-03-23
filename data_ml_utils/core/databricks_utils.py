import datetime
from typing import Dict

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
