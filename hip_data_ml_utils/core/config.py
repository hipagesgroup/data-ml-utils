from typing import Dict

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    AWS_DEFAULT_REGION: str
    AWS_DEFAULT_REGION = "ap-southeast-2"
    MODEL_SERVING_WORKLOAD_SIZE: str
    MODEL_SERVING_WORKLOAD_SIZE = "Medium"
    MODEL_SERVING_SCALE_TO_ZERO: str
    MODEL_SERVING_SCALE_TO_ZERO = "True"
    model_func_dict: Dict
    model_func_dict = {
        "sk_model": ["sklearn", "code_paths"],
        "xgb_model": ["xgboost", "code_paths"],
        "lgb_model": ["lightgbm", "code_paths"],
        "keras_model": ["keras", "code_paths"],
        "pytorch_model": ["pytorch", "code_paths"],
        "python_model": ["pyfunc", "code_path"],
    }


settings = Settings()
