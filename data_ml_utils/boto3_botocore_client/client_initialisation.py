from __future__ import annotations

import os

import boto3
import botocore
from data_ml_utils.core.config import settings


class AwsClients:
    def __init__(self):
        self.client_aws_services = boto3.Session(
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.client_sagemaker = self._initialize_sagemaker_client()
        self.client_s3_resource = self._initialize_s3_resource()
        self.client_s3 = self._initialize_s3_client()
        self.client_emr = self._initialize_emr_client()

    def _initialize_sagemaker_client(self) -> botocore.client.SageMaker:
        """
        initialise sagemaker client from boto3 session
        Returns
        -------
        botocore.client.SageMaker
            botocore client for SageMaker related services
        """
        return self.client_aws_services.client("sagemaker")

    def _initialize_s3_resource(self) -> boto3.resources.factory.s3.ServiceResource:
        """
        initialise s3 resource from boto3 session
        Returns
        -------
        boto3.resources.factory.s3.ServiceResource
            s3 services resource
        """
        return self.client_aws_services.resource("s3")

    def _initialize_s3_client(self) -> botocore.client.S3:
        """
        initialise s3 client from boto3 session
        Returns
        -------
        botocore.client.S3
            botocore client for s3 related services
        """
        return self.client_aws_services.client("s3")

    def _initialize_emr_client(self) -> botocore.client.EMR:
        """
        initialise emr client from boto3 session
        Returns
        -------
        botocore.client.EMR
            botocore client for EMR related services
        """
        return self.client_aws_services.client("emr")
