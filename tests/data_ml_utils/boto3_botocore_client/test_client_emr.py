from botocore.stub import ANY
from botocore.stub import Stubber
from mock import patch
from moto import mock_emr

from data_ml_utils.boto3_botocore_client.client_emr import AwsEMRServices


class TestEMRCreateCluster:
    """test class for creating EMR cluster"""

    @mock_emr
    def test_create_emr_cluster(
        self, get_run_job_flow_response, get_run_job_flow_parameters, aws_credentials
    ):
        """
        test function to create EMR cluster

        Parameters
        ----------
        get_run_job_flow_response
            emr run_job_flow response
        get_run_job_flow_parameters
            emr run_job_flow parameters
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if endpoint response status is successful, 200
        """
        # aws_client = AwsEMRServices()

        aws_client = AwsEMRServices()
        stubber = Stubber(aws_client.client_emr)

        stubber.add_response(
            "run_job_flow",
            get_run_job_flow_response,
            get_run_job_flow_parameters,
        )

        stubber.activate()

        response_test = aws_client.create_emr_cluster(
            master_instance_type="c3.xlarge",
            core_instance_type="c3.xlarge",
            core_instance_count=1,
            configurations=[
                {
                    "Classification": "spark-hive-site",
                    "Properties": {},
                    "Configurations": [],
                }
            ],
            applications=[{"Name": "Spark"}],
            log_uri="s3://test",
            task_id="mock_test",
            identifier="2022-01-01",
            bidprice="0.01",
            emr_version="emr-6.7.0",
        )

        assert response_test["ResponseMetadata"]["HTTPStatusCode"] == 200

    @mock_emr
    def test_create_emr_cluster_error(
        self,
        get_run_job_flow_error_response,
        get_run_job_flow_parameters,
        aws_credentials,
    ):
        """
        test function to create EMR cluster with error

        Parameters
        ----------
        get_run_job_flow_error_response
            emr run_job_flow error response
        get_run_job_flow_parameters
            emr run_job_flow parameters
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if endpoint response status is not successful, != 200
            if exception has been reached
        """
        aws_client = AwsEMRServices()

        stubber = Stubber(aws_client.client_emr)

        stubber.add_response(
            "run_job_flow",
            get_run_job_flow_error_response,
            get_run_job_flow_parameters,
        )

        stubber.activate()

        try:
            _ = aws_client.create_emr_cluster(
                master_instance_type="c3.xlarge",
                core_instance_type="c3.xlarge",
                core_instance_count=1,
                configurations=[
                    {
                        "Classification": "spark-hive-site",
                        "Properties": {},
                        "Configurations": [],
                    }
                ],
                applications=[{"Name": "Spark"}],
                log_uri="s3://test",
                task_id="mock_test",
                identifier="2022-01-01",
                bidprice="0.01",
                emr_version="emr-6.7.0",
            )

        except Exception:
            message = "Encountered Error while Launching the EMR Cluster"

        assert message == "Encountered Error while Launching the EMR Cluster"


class TestEMRCheckStatus:
    """test class for checking EMR status"""

    @mock_emr
    def test_check_emr_cluster_status(
        self, get_describe_cluster_response, aws_credentials
    ):
        """
        test function to create EMR cluster with error

        Parameters
        ----------
        get_describe_cluster_response
            emr describe_cluster response
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if returns non exit function response
        """
        aws_client = AwsEMRServices()

        stubber = Stubber(aws_client.client_emr)

        expected_params = {"ClusterId": ANY}
        stubber.add_response(
            "describe_cluster",
            get_describe_cluster_response,
            expected_params,
        )

        stubber.activate()

        cluster_response = aws_client.check_emr_cluster_status(
            "test",
        )

        assert cluster_response == 0

    @mock_emr
    def test_check_emr_cluster_status_error(
        self, get_describe_cluster_error_response, aws_credentials
    ):
        """
        test function to create EMR cluster with error

        Parameters
        ----------
        get_describe_cluster_error_response
            emr describe_cluster error response
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if returns non exit function response
        """
        aws_client = AwsEMRServices()

        stubber = Stubber(aws_client.client_emr)

        expected_params = {"ClusterId": ANY}
        stubber.add_response(
            "describe_cluster",
            get_describe_cluster_error_response,
            expected_params,
        )

        stubber.activate()

        try:
            _ = aws_client.check_emr_cluster_status(
                "test",
            )
        except Exception:
            error_response = "error stuff"

        assert error_response == "error stuff"


class TestEMRTerminateCluster:
    """test class for terminating EMR cluster"""

    @mock_emr
    def test_terminate_emr_cluster(self, aws_credentials):
        """
        test function to terminate EMR cluster

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if returns non exit function response
        """
        aws_client = AwsEMRServices()
        stubber = Stubber(aws_client.client_emr)

        stubber.add_response(
            "terminate_job_flows",
            {},
            {"JobFlowIds": ANY},
        )

        stubber.activate()

        cluster_response = aws_client.terminate_emr_cluster("test")

        assert cluster_response == 0


class TestEMRClusterId:
    """test class to get cluster id"""

    @mock_emr
    def test_get_cluster_id(self, get_list_cluster_response, aws_credentials):
        """
        test function to get cluster id

        Parameters
        ----------
        get_list_cluster_response
            emr list_cluster response
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            returns cluster id
        """
        aws_client = AwsEMRServices()

        stubber = Stubber(aws_client.client_emr)

        expected_params = {"ClusterStates": ANY}

        stubber.add_response(
            "list_clusters", get_list_cluster_response, expected_params
        )

        stubber.activate()

        cluster_response = aws_client.get_cluster_id("mock_test", "2022-01-01")

        assert cluster_response == "test"


class TestEMRMasterAddress:
    """test class to get EMR master node address"""

    @mock_emr
    def test_get_emr_master_dns_name(
        self, get_describe_cluster_response, aws_credentials
    ):
        """
        test function to get EMR master node address

        Parameters
        ----------
        get_describe_cluster_response
            emr describe_cluster response
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            returns cluster master node address
        """
        aws_client = AwsEMRServices()

        stubber = Stubber(aws_client.client_emr)

        expected_params = {"ClusterId": ANY}
        stubber.add_response(
            "describe_cluster",
            get_describe_cluster_response,
            expected_params,
        )

        stubber.activate()

        cluster_response = aws_client.get_emr_master_dns_name("test")

        assert cluster_response == "ec2-13-50-100.aws.com"


class TestEMRSpinUpCluster:
    """test class to create EMR cluster"""

    @mock_emr
    @patch(
        "data_ml_utils.boto3_botocore_client.client_emr.AwsEMRServices.create_emr_cluster"  # noqa E501
    )
    def test_spin_up_emr_cluster(
        self, mocked_create_emr_cluster, get_describe_cluster_response, aws_credentials
    ):
        """
        test function to create EMR cluster and check if master node address
        is compliant to how it will work

        Parameters
        ----------
        mocked_create_emr_cluster
            mocked create emr cluster function
        get_describe_cluster_response
            emr describe_cluster response
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if returns non exit function response
        """
        aws_client = AwsEMRServices()

        mocked_create_emr_cluster.return_value = {"JobFlowId": "test"}

        stubber = Stubber(aws_client.client_emr)

        expected_params = {"ClusterId": ANY}
        stubber.add_response(
            "describe_cluster",
            get_describe_cluster_response,
            expected_params,
        )

        stubber.add_response(
            "describe_cluster",
            get_describe_cluster_response,
            expected_params,
        )

        stubber.activate()

        response_test = aws_client.spin_up_emr_cluster(
            master_instance_type="c3.xlarge",
            core_instance_type="c3.xlarge",
            core_instance_count=1,
            configurations=[
                {
                    "Classification": "spark-hive-site",
                    "Properties": {},
                    "Configurations": [],
                }
            ],
            applications=[{"Name": "Spark"}],
            log_uri="s3://test",
            task_id="mock_test",
            identifier="2022-01-01",
            bidprice="0.01",
            emr_version="emr-6.7.0",
        )

        assert response_test == 0
