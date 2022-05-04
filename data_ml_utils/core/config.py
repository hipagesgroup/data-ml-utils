from pydantic import BaseSettings


class Settings(BaseSettings):

    S3_ATHENA_QUERY_DIRECTORY: str
    S3_ATHENA_QUERY_DIRECTORY = (
        "s3://au-com-hipages-offline-feature-store/athena_queries/"
    )
    AWS_DEFAULT_REGION: str
    AWS_DEFAULT_REGION = "ap-southeast-2"


settings = Settings()
