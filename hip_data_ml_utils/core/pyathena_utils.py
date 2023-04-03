import pathlib
from typing import Tuple

import yaml


# function to read sql file
def read_sql(file_path: str) -> str:
    """
    reads sql file and return string

    Parameters
    ----------
    file_path : str
        file path of sql file

    Returns
    -------
    str
        query string of sql file
    """
    return pathlib.Path(file_path).read_text()


# function to get yaml config values
def get_config_yaml(file_path: str) -> Tuple[str, str, str, str, str, str]:
    """
    get values in yaml config

    Parameters
    ----------
    file_path : str
        file path of yaml schema

    Returns
    -------
    str
        table name
    str
        table description
    str
        table column name
    str
        name of partition column
    str
        comment for partition column
    str
        s3 bucket
    """
    with open(file_path) as file:
        config_yaml = yaml.safe_load(file)

    table_name = f"{config_yaml['schema']}.{config_yaml['tables'][0]['name']}"

    table_description = f"{config_yaml['tables'][0]['description']}"

    list_columns = []
    for i in config_yaml["tables"][0]["columns"]:

        if "partition" in i["description"]:
            partition_column = i["name"]
            partition_column_comment = i["description"]
            continue

        string_value = (
            f"{i['name']} {i['data_type'].upper()} COMMENT '{i['description']}'"
        )
        list_columns.append(string_value)

    table_column_name = ",\n".join(list_columns)
    s3_bucket = (
        f"{config_yaml['tables'][0]['s3_bucket']}/{config_yaml['tables'][0]['folder']}/"
    )

    return (
        table_name,
        table_description,
        table_column_name,
        partition_column,
        partition_column_comment,
        s3_bucket,
    )


# function to format create schema or repair table
def format_sql_create_schema(sql: str, yaml_file_path: str) -> Tuple[str, str]:
    """
    format sql create table to input parameters

    Parameters
    ----------
    sql : str
        loaded sql with input parameters
    yaml_file_path : str
        yaml file path

    Returns
    -------
    str
        formatted sql with input parameters
    """

    (
        table_name,
        table_description,
        table_column_name,
        partition_column,
        partition_column_comment,
        s3_bucket,
    ) = get_config_yaml(yaml_file_path)

    return_sql = sql.format(
        table_name=table_name,
        table_column_name=table_column_name,
        table_description=table_description,
        partitioned_column=partition_column,
        partitioned_column_comment=partition_column_comment,
        s3_bucket=s3_bucket,
    )

    return return_sql, table_name


def format_sql_repair_table(sql: str, table_name: str) -> str:
    """
    format sql repair table to input parameters

    Parameters
    -----------
    sql : str
        loaded sql with input parameters
    table_name : str
        name of table

    Returns
    -------
    str
        formatted sql with input parameters
    """

    return sql.format(table_name=table_name)
