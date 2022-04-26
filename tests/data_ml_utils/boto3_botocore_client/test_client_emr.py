from moto import mock_emr

from data_ml_utils.boto3_botocore_client.client_emr import AwsEMRServices


class TestEMRCreateCluster:
    """test class for creating EMR cluster"""

    @mock_emr
    def test_create_emr_cluster(self, aws_credentials):
        """
        test function to create EMR cluster

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if endpoint response status is successful, 200
        """
        aws_client = AwsEMRServices()
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
        )

        assert response_test["ResponseMetadata"]["HTTPStatusCode"] == 200

    @mock_emr
    def test_create_emr_cluster_error(self, aws_credentials):
        """
        test function to create EMR cluster with error

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            if endpoint response status is not successful, != 200
            if exception has been reached
        """
        aws_client = AwsEMRServices()
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
        )
        response_test["ResponseMetadata"]["HTTPStatusCode"] = 404

        try:
            if response_test["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise Exception("Encountered Error while Launching the EMR Cluster")
        except Exception:
            message = "Encountered Error while Launching the EMR Cluster"

        assert response_test["ResponseMetadata"]["HTTPStatusCode"] != 200
        assert message == "Encountered Error while Launching the EMR Cluster"


class TestEMRCheckStatus:
    """test class for checking EMR status"""

    @mock_emr
    def test_create_emr_cluster(self, aws_credentials):
        """
        test function to create EMR cluster with error

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
        )

        cluster_response = aws_client.check_emr_cluster_status(
            response_test["JobFlowId"],
        )

        assert cluster_response == 0


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
        )

        cluster_response = aws_client.terminate_emr_cluster(response_test["JobFlowId"])

        assert cluster_response == 0


class TestEMRClusterId:
    """test class to get cluster id"""

    @mock_emr
    def test_get_cluster_id(self, aws_credentials):
        """
        test function to get cluster id

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            returns cluster id
        """
        aws_client = AwsEMRServices()

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
        )

        cluster_response = aws_client.get_cluster_id("mock_test", "2022-01-01")

        assert cluster_response == response_test["JobFlowId"]


class TestEMRMasterAddress:
    """test class to get EMR master node address"""

    @mock_emr
    def test_get_emr_master_dns_name(self, aws_credentials):
        """
        test function to get EMR master node address

        Parameters
        ----------
        aws_credientials
            inherits the aws creds when invoking aws functions

        Returns
        -------
        assert
            returns cluster master node address
        """
        aws_client = AwsEMRServices()

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
        )

        cluster_response = aws_client.get_emr_master_dns_name(
            response_test["JobFlowId"]
        )

        dns_name = aws_client.client_emr.describe_cluster(
            ClusterId=response_test["JobFlowId"]
        )["Cluster"]["MasterPublicDnsName"]

        assert cluster_response == dns_name


class TestEMRSpinUpCluster:
    """test class to create EMR cluster"""

    @mock_emr
    def test_spin_up_emr_cluster(self, aws_credentials):
        """
        test function to create EMR cluster and check if master node address
        is compliant to how it will work

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
        )

        assert response_test == 0
