import tarfile
from typing import Dict
from typing import Tuple

from data_ml_utils.boto3_botocore_client.client_initialisation import AwsClients


class AwsSagemakerServices:
    """
    Class that handles all aws sagemaker related services
    """

    def __init__(self):
        client_class = AwsClients()
        self.client_sagemaker = client_class.client_sagemaker
        self.client_s3_resource = client_class.client_s3_resource
        self.client_s3 = client_class.client_s3

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
        self,
        file_targz: str,
        bucket_name_trunc: str,
        targz_file_uri: str,
        s3_file_path: str,
    ) -> int:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        file_targz : str
            model tar gz file name
        bucket_name_trunc: str
            truncated s3 bucket directory
        targz_file_uri: str
            targz file full s3 uri
        s3_file_path: str
            file path to file in s3 bucket

        Returns
        -------
        int
            if successful returns non exit function value
        """
        self.client_s3_resource.Bucket(bucket_name_trunc).download_file(
            f"{s3_file_path}/{file_targz}", file_targz
        )

        with tarfile.open(file_targz) as open_file:
            open_file.extractall(".")

        return 0

    def upload_retrained_model_s3(
        self,
        date_format: str,
        bucket_name_trunc: str,
        s3_file_path: str,
        model_suffix: str,
    ) -> str:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        date_format : str
            date format for file name
        bucket_name_trunc : str
            truncated name of s3 bucket
        s3_file_path: str
            file path to file in s3 bucket
        model_suffix: str
            model file name suffix

        Returns
        -------
        str
            name of model tar gz file
        """
        model_file_name = f"{model_suffix}_{date_format}.tar.gz"

        with tarfile.open(f"{model_file_name}", mode="w:gz") as archive:
            archive.add("model_files", recursive=True)

        self.client_s3.upload_file(
            Filename=f"{model_file_name}",
            Bucket=f"{bucket_name_trunc}",
            Key=f"{s3_file_path}/{model_file_name}",
        )

        return model_file_name

    def create_model_package_version(
        self,
        model_name: str,
        model_file_name: str,
        current_retrained_model_metrics_dict: Dict,
        s3_directory: str,
        image_uri: str,
        model_package_description: str,
    ) -> int:
        """
        gets model tar gz uri and filename from AWS model registry
        Parameters
        ----------
        model_name : str
            name of model in AWS model registry
        model_file_name : str
            model tar gz file path in s3
        current_retrained_model_metrics_dict : Dict
            current and retrained model metrics in dictionary
        s3_directory : str
            s3 bucket for model
        image_uri : str
            docker image url
        model_package_description: str
            model package description

        Returns
        -------
        int
            non exit function
        """
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
            model_url = f"{s3_directory}{model_file_name}"

            modelpackage_inference_specification["InferenceSpecification"][
                "Containers"
            ][0]["ModelDataUrl"] = model_url

            modelpackage_custom_metadata = {
                "CustomerMetadataProperties": current_retrained_model_metrics_dict
            }

            create_model_package_input_dict = {
                "ModelPackageGroupName": f"{model_name}",
                "ModelPackageDescription": f"{model_package_description}",
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
