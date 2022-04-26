import filecmp

import botocore
from botocore.exceptions import ParamValidationError
from botocore.exceptions import StubAssertionError
from botocore.stub import ANY
from botocore.stub import Stubber
from moto import mock_s3
from moto import mock_sagemaker

from data_ml_utils.boto3_botocore_client.client_sagemaker import AwsSagemakerServices

orig = botocore.client.BaseClient._make_api_call


class TestAWSServices:
    """test class for AWS session"""

    def test_get_model_uri_from_aws_model_registry(
        self,
        aws_credentials,
        get_describe_model_package_response,
        get_approved_list_package,
    ):
        """
        test function to retrieve model uri from sagemaker model registry

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions
        get_describe_model_package_response
            sagemaker describe_model_package response
        get_approved_list_package
            sagemaker list_model_packages response, approved

        Returns
        -------
        assert
            if file name is the same
        """

        mock = mock_sagemaker()
        mock.start()
        aws_client = AwsSagemakerServices()

        stubber = Stubber(aws_client.client_sagemaker)

        expected_params = {"ModelPackageGroupName": ANY}
        stubber.add_response(
            "list_model_packages", get_approved_list_package, expected_params
        )
        expected_params_ = {"ModelPackageName": ANY}
        stubber.add_response(
            "describe_model_package",
            get_describe_model_package_response,
            expected_params_,
        )
        stubber.activate()

        test_uri, test_file = aws_client.get_model_uri_from_aws_model_registry(
            "churn-test"
        )

        mock.stop()

        assert test_file == "model_testing.tar.gz"

    def test_get_model_uri_from_aws_model_registry_error_approved(
        self,
        aws_credentials,
        get_describe_model_package_response,
        get_rejected_list_package,
    ):
        """
        test function to retrieve model uri from sagemaker model registry

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions
        get_describe_model_package_response
            sagemaker describe_model_package response
        get_rejected_list_package
            sagemaker list_model_packages response, rejected

        Returns
        -------
        assert
            captures ParamValidationError
        """

        mock = mock_sagemaker()
        mock.start()
        aws_client = AwsSagemakerServices()

        stubber = Stubber(aws_client.client_sagemaker)

        expected_params = {"ModelPackageGroupName": ANY}
        stubber.add_response(
            "list_model_packages", get_rejected_list_package, expected_params
        )
        expected_params_ = {"ModelPackageName": ANY}
        stubber.add_response(
            "describe_model_package",
            get_describe_model_package_response,
            expected_params_,
        )
        stubber.activate()

        try:
            _, _ = aws_client.get_model_uri_from_aws_model_registry("churn-test")
        except ParamValidationError:
            message = "ModelGroupName does not have approved status"

        mock.stop()

        assert message == "ModelGroupName does not have approved status"

    def test_get_model_uri_from_aws_model_registry_invalid_modelname(
        self,
        aws_credentials,
        get_describe_model_package_response,
        get_approved_list_package,
    ):
        """
        test function to retrieve model uri from sagemaker model registry

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions
        get_describe_model_package_response
            sagemaker describe_model_package response
        get_approved_list_package
            sagemaker list_model_packages response, approved

        Returns
        -------
        assert
            captures ParamValidationError
        """

        mock = mock_sagemaker()
        mock.start()
        aws_client = AwsSagemakerServices()

        stubber = Stubber(aws_client.client_sagemaker)

        expected_params = {"ModelPackageGroupName": "churn-test"}
        stubber.add_response(
            "list_model_packages", get_approved_list_package, expected_params
        )
        expected_params_ = {"ModelPackageName": "churn-test"}
        stubber.add_response(
            "describe_model_package",
            get_describe_model_package_response,
            expected_params_,
        )
        stubber.activate()

        try:
            _, _ = aws_client.get_model_uri_from_aws_model_registry("churn-prod")
        except StubAssertionError:
            message = "incorrect model group name"

        mock.stop()

        assert message == "incorrect model group name"

    def test_unzip_targz_file(self, aws_credentials):
        """
        test function to unzip tar gz file

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if returns non exit function value
        """

        mock = mock_s3()
        mock.start()
        aws_client = AwsSagemakerServices()
        # create bucket
        aws_client.client_s3.create_bucket(
            Bucket="au-com-hipages-radagast",
            CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
        )

        aws_client.client_s3_resource.meta.client.upload_file(
            "tests/dummy.tar.gz",
            "au-com-hipages-radagast",
            "scratchpad/muriel/models/2022_01_01/dummy.tar.gz",
        )

        response_result = aws_client.unzip_targz_file(
            "dummy.tar.gz",
            "au-com-hipages-radagast",
            "scratchpad/muriel/models/2022_01_01/dummy.tar.gz",
            "scratchpad/muriel/models/2022_01_01",
        )

        mock.stop()

        assert response_result == 0
        assert filecmp.cmp("dummy.tar.gz", "tests/dummy.tar.gz")

    def test_upload_retrained_model_s3(self, aws_credentials):
        """
        test function to upload retrained model to s3

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if model file name is as expected
        """
        mock = mock_s3()
        mock.start()
        aws_client = AwsSagemakerServices()

        aws_client.client_s3.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
        )

        test_file = aws_client.upload_retrained_model_s3(
            "2022_01_01", "test-bucket", "", "model_muriel"
        )

        mock.stop()

        assert test_file == "model_muriel_2022_01_01.tar.gz"

    def test_create_model_package_version_error(self, aws_credentials):
        """
        test function to create model package version in AWS model registry

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if response is as expected
        """
        mock = mock_sagemaker()
        mock.start()
        aws_client = AwsSagemakerServices()

        retrained_model_metrics_dict = {
            "accuracy_top_10": 1.0,
        }

        current_model_metrics_dict = {
            "accuracy_top_10": 0.9,
        }

        stubber = Stubber(aws_client.client_sagemaker)

        create_model_package_response = {"ModelPackageArn": "test"}
        expected_params = {"ModelPackageGroupName": ANY}
        stubber.add_response(
            "create_model_package", create_model_package_response, expected_params
        )

        try:
            aws_client.create_model_package_version(
                "churn-test",
                "model_123.tar.gz",
                retrained_model_metrics_dict,
                current_model_metrics_dict,
                "test-bucket",
                "testing",
            )
        except Exception:
            message = "error message"

        mock.stop()

        assert message == "error message"

    def test_create_model_package_version(self, aws_credentials):
        """
        test function to create model package version in AWS model registry

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if response is as expected
        """
        mock = mock_sagemaker()
        mock.start()
        aws_client = AwsSagemakerServices()

        current_retrained_model_metrics_dict = {
            "retrained_top_10_accuracy": "1.0",
            "current_top_10_accuracy": "1.0",
        }

        stubber = Stubber(aws_client.client_sagemaker)

        create_model_package_response = {"ModelPackageArn": "test"}
        expected_params = {
            "CustomerMetadataProperties": ANY,
            "InferenceSpecification": ANY,
            "ModelApprovalStatus": ANY,
            "ModelPackageDescription": ANY,
            "ModelPackageGroupName": ANY,
        }
        stubber.add_response(
            "create_model_package", create_model_package_response, expected_params
        )
        stubber.activate()

        response = aws_client.create_model_package_version(
            "churn-test",
            "model_123.tar.gz",
            current_retrained_model_metrics_dict,
            "test-bucket/",
            "testing",
            "description",
        )

        mock.stop()

        assert response == 0
