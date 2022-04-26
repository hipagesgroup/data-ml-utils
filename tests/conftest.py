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
    list_model_packages_response = {
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
    return list_model_packages_response


@pytest.fixture(autouse=True)
def get_approved_list_package():
    list_model_packages_response = {
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
    return list_model_packages_response


@pytest.fixture(autouse=True)
def get_describe_model_package_response():
    describe_model_package_response = {
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
    return describe_model_package_response
