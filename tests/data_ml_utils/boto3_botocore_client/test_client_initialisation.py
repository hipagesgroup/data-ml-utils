import boto3
import botocore
from mock import patch
from moto import mock_sagemaker

from data_ml_utils.boto3_botocore_client.client_initialisation import AwsClients

orig = botocore.client.BaseClient._make_api_call


class TestAwsClients:
    """test class for AWS Clients"""

    def test_boto3_session(self, aws_credentials):
        """
        test function to initialise a boto3 session

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if class session is boto3.session.Session
        """
        bc_session_patch = patch("boto3.session.Session")
        bc_session_cls = bc_session_patch.start()
        loader = bc_session_cls.return_value.get_component.return_value
        loader.data_path = ""
        patch_global_session = patch("boto3.DEFAULT_SESSION")
        patch_global_session.start()

        assert bc_session_cls == boto3.session.Session

    @mock_sagemaker
    def test_initialize_sagemaker_client(self, aws_credentials):
        """
        test function to initialise a sagemaker session

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if class session is botocore.client.SageMaker
        """
        aws_client = AwsClients()
        sagemaker_session = aws_client.client_sagemaker

        assert "botocore.client.SageMaker" in str(type(sagemaker_session))
