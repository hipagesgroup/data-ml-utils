import os
import tarfile
from typing import Dict
from typing import Tuple

import boto3
import botocore


class AwsServices:
    def __init__(self):
        self.client_aws_services = boto3.Session(
            region_name="ap-southeast-2",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.client_sagemaker = self._initialize_sagemaker_client()
        self.client_s3_resource = self._initialize_s3_resource()
        self.client_s3 = self._initialize_s3_client()

    def _initialize_sagemaker_client(self) -> "botocore.client.SageMaker":
        """
        initialise sagemaker client from boto3 session
        Returns
        -------
        botocore.client.SageMaker
            botocore client for SageMaker related services
        """
        return self.client_aws_services.client("sagemaker")

    def _initialize_s3_resource(self) -> "boto3.resources.factory.s3.ServiceResource":
        """
        initialise s3 resource from boto3 session
        Returns
        -------
        boto3.resources.factory.s3.ServiceResource
            s3 services resource
        """
        return self.client_aws_services.resource("s3")

    def _initialize_s3_client(self) -> "botocore.client.S3":
        """
        initialise s3 client from boto3 session
        Returns
        -------
        botocore.client.S3
            botocore client for s3 related services
        """
        return self.client_aws_services.client("s3")

    def get_model_uri_from_aws_model_registry(self, model_name: str) -> Tuple[str, str]:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        model_name : str
            name of churn model on AWS model registry

        Returns
        -------
        str
            model tar gz s3 file uri
        str
            model tar gz file name
        """
        response = self.client_sagemaker.list_model_packages(
            ModelPackageGroupName=model_name
        )

        model_arn = ""
        for i in response["ModelPackageSummaryList"]:
            if i["ModelApprovalStatus"] == "Approved":
                model_arn = i["ModelPackageArn"]

        targz_file_uri = self.client_sagemaker.describe_model_package(
            ModelPackageName=model_arn
        )["InferenceSpecification"]["Containers"][0]["ModelDataUrl"]

        file = targz_file_uri.split("/")[-1]

        return targz_file_uri, file

    def unzip_targz_file(
        self, file_targz: str, bucket_name_trunc: str, targz_file_uri: str
    ) -> int:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        file_targz : str
            model tar gz file name
        bucket_name_trunc: str
            truncated s3 muriel bucket directory
        targz_file_uri: str
            targz file full s3 uri

        Returns
        -------
        int
            if successful returns non exit function value
        """
        date_to_use = targz_file_uri.split("/")[-2]
        self.client_s3_resource.Bucket(bucket_name_trunc).download_file(
            f"scratchpad/muriel/models/{date_to_use}/{file_targz}", file_targz
        )

        open_file = tarfile.open(file_targz)
        open_file.extractall(".")

        return 0

    def upload_retrained_model_s3(
        self,
        start_date: str,
        bucket_name_trunc: str,
    ) -> str:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        start_date : str
            arg parser start date
        bucket_name_trunc : str
            truncated name of churn prediction bucket

        Returns
        -------
        str
            name of model tar gz file
        """
        format_start_date = start_date.replace("-", "_")
        model_file_name = f"model_muriel_{format_start_date}.tar.gz"

        with tarfile.open(f"{model_file_name}", mode="w:gz") as archive:
            archive.add("model_files", recursive=True)

        self.client_s3.upload_file(
            Filename=f"{model_file_name}",
            Bucket=f"{bucket_name_trunc}",
            Key=f"scratchpad/muriel/models/{format_start_date}/{model_file_name}",
        )

        return model_file_name

    def create_model_package_version(
        self,
        start_date: str,
        model_name: str,
        model_file_name: str,
        retrained_model_metrics_dict: Dict,
        current_model_metrics_dict: Dict,
        muriel_s3: str,
        image_uri: str,
    ) -> int:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        start_date : str
            arg parser start date
        model_name : str
            name of churn model in AWS model registry
        model_file_name : str
            model tar gz file path in s3
        model_metrics_dict : Dict
            churn model metrics in dictory
        muriel_s3 : str
            s3 bucket for churn prediction
        image_uri : str
            docker image url

        Returns
        -------
        int
            non exit function
        """
        format_start_date = start_date.replace("-", "_")
        try:
            modelpackage_inference_specification = {
                "InferenceSpecification": {
                    "Containers": [
                        {
                            "Image": f"{image_uri}",
                        }
                    ],
                    "SupportedContentTypes": ["text/csv"],
                    "SupportedResponseMIMETypes": ["text/csv"],
                }
            }
            model_url = (
                f"""{muriel_s3}scratchpad/muriel/models/"""
                f"""{format_start_date}/{model_file_name}"""
            )

            modelpackage_inference_specification["InferenceSpecification"][
                "Containers"
            ][0]["ModelDataUrl"] = model_url

            modelpackage_custom_metadata = {
                "CustomerMetadataProperties": {
                    "retrained_top_10_accuracy": str(
                        retrained_model_metrics_dict["accuracy_top_10"]
                    ),
                    "current_top_10_accuracy": str(
                        current_model_metrics_dict["accuracy_top_10"]
                    ),
                }
            }

            create_model_package_input_dict = {
                "ModelPackageGroupName": f"{model_name}",
                "ModelPackageDescription": "Naive bayes model for category prediction from get_quotes keywords",  # noqa E501
                "ModelApprovalStatus": "PendingManualApproval",
            }

            create_model_package_input_dict.update(modelpackage_inference_specification)
            create_model_package_input_dict.update(modelpackage_custom_metadata)

            create_model_package_response = self.client_sagemaker.create_model_package(
                **create_model_package_input_dict
            )
            print(create_model_package_response["ModelPackageArn"])
        except Exception:
            raise Exception("error in uploading creating version in model registry")

        return 0
