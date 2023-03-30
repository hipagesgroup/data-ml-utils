from pydantic import BaseSettings


class Settings(BaseSettings):

    S3_ATHENA_QUERY_DIRECTORY: str
    S3_ATHENA_QUERY_DIRECTORY = (
        "s3://au-com-hipages-offline-feature-store/athena_queries/"
    )
    AWS_DEFAULT_REGION: str
    AWS_DEFAULT_REGION = "ap-southeast-2"
    model_func_dict = {
        "sk_model": ["sklearn", "code_paths"],
        "xgb_model": ["xgboost", "code_paths"],
        "lgb_model": ["lightgbm", "code_paths"],
        "keras_model": ["keras", "code_paths"],
        "pytorch_model": ["pytorch", "code_paths"],
        "python_model": ["pyfunc", "code_path"],
    }


settings = Settings()