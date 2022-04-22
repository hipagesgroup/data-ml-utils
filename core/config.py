from pydantic import BaseSettings


class Settings(BaseSettings):

    S3_ATHENA_QUERY_DIRECTORY: str
    S3_ATHENA_QUERY_DIRECTORY = (
        "s3://au-com-hipages-offline-feature-store/athena_queries/"
    )


settings = Settings()
