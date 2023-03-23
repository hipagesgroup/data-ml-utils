import datetime
import os
from unittest.mock import patch

import pytest


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # pragma: allowlist secret
    os.environ[  # pragma: allowlist secret
        "AWS_SECRET_ACCESS_KEY"  # noqa: S105
    ] = "testing"
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


@pytest.fixture(autouse=True)
def get_run_job_flow_response():
    return {
        "JobFlowId": "test",
        "ClusterArn": "arn:aws:elasticmapreduce:ap-southeast-2:2512598797:cluster/test",
        "ResponseMetadata": {
            "RequestId": "fcce68e3-7d3e-4d27-bc55-ad46f52afa21",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "fcce68e3-7d3e-4d27-bc55-ad46f52afa21",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "121",
                "date": "Thu, 04 Aug 2022 03:35:46 GMT",
            },
            "RetryAttempts": 0,
        },
    }


@pytest.fixture(autouse=True)
def get_run_job_flow_error_response():
    return {
        "JobFlowId": "test",
        "ClusterArn": "arn:aws:elasticmapreduce:ap-southeast-2:2512598797:cluster/test",
        "ResponseMetadata": {
            "RequestId": "fcce68e3-7d3e-4d27-bc55-ad46f52afa21",
            "HTTPStatusCode": 502,
            "HTTPHeaders": {
                "x-amzn-requestid": "fcce68e3-7d3e-4d27-bc55-ad46f52afa21",
                "content-type": "application/x-amz-json-1.1",
                "content-length": "121",
                "date": "Thu, 04 Aug 2022 03:35:46 GMT",
            },
            "RetryAttempts": 0,
        },
    }


@pytest.fixture(autouse=True)
def get_run_job_flow_parameters():
    return {
        "Applications": [{"Name": "Spark"}],
        "AutoTerminationPolicy": {"IdleTimeout": 1200},
        "Configurations": [
            {
                "Classification": "spark-hive-site",
                "Configurations": [],
                "Properties": {},
            }
        ],
        "EbsRootVolumeSize": 50,
        "Instances": {
            "Ec2KeyName": "hipages-data-team",
            "EmrManagedMasterSecurityGroup": "sg-96e9ebf0",
            "EmrManagedSlaveSecurityGroup": "sg-51e9eb37",
            "InstanceFleets": [
                {
                    "InstanceFleetType": "MASTER",
                    "InstanceTypeConfigs": [
                        {"InstanceType": "c3.xlarge", "WeightedCapacity": 1}
                    ],
                    "Name": "master_fleet",
                    "TargetOnDemandCapacity": 1,
                },
                {
                    "InstanceFleetType": "CORE",
                    "InstanceTypeConfigs": [
                        {
                            "BidPrice": "0.01",
                            "InstanceType": "c3.xlarge",
                            "WeightedCapacity": 1,
                        }
                    ],
                    "LaunchSpecifications": {
                        "SpotSpecification": {
                            "TimeoutAction": "SWITCH_TO_ON_DEMAND",
                            "TimeoutDurationMinutes": 5,
                        }
                    },
                    "Name": "core_fleet",
                    "TargetSpotCapacity": 1,
                },
            ],
            "KeepJobFlowAliveWhenNoSteps": True,
            "TerminationProtected": False,
        },
        "JobFlowRole": "EMR_EC2_DefaultRole",
        "LogUri": "s3://test",
        "ManagedScalingPolicy": {
            "ComputeLimits": {
                "MaximumCapacityUnits": 120,
                "MaximumCoreCapacityUnits": 120,
                "MaximumOnDemandCapacityUnits": 0,
                "MinimumCapacityUnits": 60,
                "UnitType": "InstanceFleetUnits",
            }
        },
        "Name": "churn__mock_test__2022-01-01",
        "ReleaseLabel": "emr-6.7.0",
        "ScaleDownBehavior": "TERMINATE_AT_TASK_COMPLETION",
        "ServiceRole": "EMR_DefaultRole",
        "Steps": [
            {
                "ActionOnFailure": "TERMINATE_CLUSTER",
                "HadoopJarStep": {
                    "Args": ["state-pusher-script"],
                    "Jar": "command-runner.jar",
                },
                "Name": "Spark application",
            },
            {
                "ActionOnFailure": "TERMINATE_CLUSTER",
                "HadoopJarStep": {
                    "Args": [
                        "s3://au-com-hipages-data-scratchpad/shuming-development/jar_file/copy_isolation_jar_emr_cluster.sh"  # noqa E501
                    ],
                    "Jar": "s3://ap-southeast-2.elasticmapreduce/libs/script-runner/script-runner.jar",  # noqa E501
                },
                "Name": "Custom JAR",
            },
        ],
        "VisibleToAllUsers": True,
    }


@pytest.fixture
def mock_active_run():
    """mocked mlflow.active_run()"""

    with patch(
        "data_ml_utils.mlflow_databricks.mlflow_tracker.mlflow.active_run"
    ) as mock_active_run:
        mock_active_run.return_value = None
        yield mock_active_run
