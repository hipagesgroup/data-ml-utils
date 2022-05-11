import datetime
import os

import pytest


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # pragma: allowlist secret
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # pragma: allowlist secret
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"  # pragma: allowlist secret


@pytest.fixture(autouse=True)
def get_rejected_list_package():
    return {
        "ModelPackageSummaryList": [
            {
                "ModelPackageName": "churn-test",
                "ModelPackageArn": "test",
                "CreationTime": datetime.datetime(2022, 1, 1),
                "ModelPackageStatus": "Completed",
                "ModelApprovalStatus": "Rejected",
            }
        ]
    }


@pytest.fixture(autouse=True)
def get_approved_list_package():
    return {
        "ModelPackageSummaryList": [
            {
                "ModelPackageName": "churn-test",
                "ModelPackageArn": "test",
                "CreationTime": datetime.datetime(2022, 1, 1),
                "ModelPackageStatus": "Completed",
                "ModelApprovalStatus": "Approved",
            }
        ]
    }


@pytest.fixture(autouse=True)
def get_describe_model_package_response():
    return {
        "ModelPackageName": "churn-test",
        "ModelPackageArn": "test",
        "CreationTime": datetime.datetime(2022, 1, 1),
        "ModelPackageStatus": "Completed",
        "ModelPackageStatusDetails": {
            "ValidationStatuses": [
                {
                    "Name": "whatever",
                    "Status": "Completed",
                    "FailureReason": "string",
                },
            ],
        },
        "InferenceSpecification": {
            "Containers": [
                {
                    "ModelDataUrl": "whatever/model_testing.tar.gz",
                    "Image": "urltest",
                }
            ],
            "SupportedContentTypes": ["str"],
            "SupportedResponseMIMETypes": ["str"],
        },
    }


@pytest.fixture(autouse=True)
def get_list_cluster_response():
    return {
        "Clusters": [
            {
                "Id": "test",
                "Name": "churn__mock_test__2022-01-01",
                "Status": {
                    "State": "WAITING",
                    "StateChangeReason": {"Code": "ALL_STEPS_COMPLETED"},
                },
            }
        ]
    }


@pytest.fixture(autouse=True)
def get_describe_cluster_response():
    return {
        "Cluster": {
            "Id": "test",
            "Name": "churn__mock_test__2022-01-01",
            "Status": {
                "State": "WAITING",
                "StateChangeReason": {"Code": "ALL_STEPS_COMPLETED"},
            },
            "MasterPublicDnsName": "ec2-13-50-100.aws.com",
        }
    }


@pytest.fixture(autouse=True)
def get_describe_cluster_error_response():
    return {
        "Cluster": {
            "Id": "test",
            "Name": "churn__mock_test__2022-01-01",
            "Status": {
                "State": "TERMINATED_WITH_ERRORS",
                "StateChangeReason": {"Code": "ALL_STEPS_COMPLETED"},
            },
            "MasterPublicDnsName": "ec2-1-50-100.aws.com",
        }
    }
