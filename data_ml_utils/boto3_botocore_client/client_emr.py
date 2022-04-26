import os
import sys
import time
from typing import List

import boto3
import botocore


class AwsServicesEMR:
    """
    Class that handles all aws related services
    This includes creating of EMR cluster, terminating cluster,
    retrieving status and ip address of cluster
    Initialisation of class returns the boto3 session and emr client
    """

    def __init__(self):
        self.client_aws_services = boto3.Session(
            region_name="ap-southeast-2",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.client_emr = self._initialize_emr_client()

    def _initialize_emr_client(self) -> "botocore.client.EMR":
        """
        initialise emr client from boto3 session
        Returns
        -------
        botocore.client.EMR
            botocore client for EMR related services
        """
        return self.client_aws_services.client("emr")

    def create_emr_cluster(
        self,
        session: "botocore.client.EMR",
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str,
    ) -> dict:
        """
        creates EMR cluster

        Parameters
        ----------
        session : botocore.client.EMR
            session of EMR
        master_instance_type: str
            master instance type
        core_instance_type: str
            core instance type
        core_instance_count: int
            number of core instances
        configurations: List
            configurations of creating cluster
        applications: List
            applications that should be created for the cluster
        log_uri: str
            s3 directory of logs
        task_id: str
            airflow task id
        identifier: str
            identifier date
        bidprice: str
            bidprice of spot instances

        Returns
        -------
        dict
            response of request of creating cluster, raises exception if not successful
        """
        response = session.run_job_flow(
            Name=f"churn__{task_id}__{identifier}",
            LogUri=log_uri,
            ReleaseLabel="emr-6.1.0",
            Instances={
                "InstanceFleets": [
                    {
                        "Name": "master_fleet",
                        "InstanceFleetType": "MASTER",
                        "TargetOnDemandCapacity": 1,
                        "InstanceTypeConfigs": [
                            {
                                "InstanceType": master_instance_type,
                                "WeightedCapacity": 1,
                            },
                        ],
                    },
                    {
                        "Name": "core_fleet",
                        "InstanceFleetType": "CORE",
                        "TargetSpotCapacity": int(core_instance_count),
                        "InstanceTypeConfigs": [
                            {
                                "InstanceType": core_instance_type,
                                "WeightedCapacity": 1,
                                "BidPrice": bidprice,
                            },
                        ],
                        "LaunchSpecifications": {
                            "SpotSpecification": {
                                "TimeoutDurationMinutes": 20,
                                "TimeoutAction": "SWITCH_TO_ON_DEMAND",
                            }
                        },
                    },
                ],
                "Ec2KeyName": "hipages-data-team",
                "KeepJobFlowAliveWhenNoSteps": True,
                "TerminationProtected": False,
                "EmrManagedMasterSecurityGroup": "sg-96e9ebf0",
                "EmrManagedSlaveSecurityGroup": "sg-51e9eb37",
            },
            EbsRootVolumeSize=50,
            Steps=[
                {
                    "Name": "Spark application",
                    "ActionOnFailure": "TERMINATE_CLUSTER",
                    "HadoopJarStep": {
                        "Jar": "command-runner.jar",
                        "Args": ["state-pusher-script"],
                    },
                },
                {
                    "Name": "Custom JAR",
                    "ActionOnFailure": "TERMINATE_CLUSTER",
                    "HadoopJarStep": {
                        "Jar": "s3://ap-southeast-2.elasticmapreduce/libs/script-runner/script-runner.jar",  # noqa E501
                        "Args": [
                            "s3://au-com-hipages-data-scratchpad/shuming-development/jar_file/copy_isolation_jar_emr_cluster.sh"  # noqa E501
                        ],
                    },
                },
            ],
            Applications=applications,
            Configurations=configurations,
            JobFlowRole="EMR_EC2_DefaultRole",
            VisibleToAllUsers=True,
            ServiceRole="EMR_DefaultRole",
            ScaleDownBehavior="TERMINATE_AT_TASK_COMPLETION",
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(  # pragma: no cover
                f"Encountered Error while Launching the EMR Cluster \n {response}"
            )
            sys.exit(1)  # pragma: no cover

        return response

    def check_emr_cluster_status(
        self, session: "botocore.client.EMR", cluster_id: str
    ) -> int:
        """
        check emr cluster that is created
        raises exception if the cluster runs into termination issues

        Parameters
        ----------
        session : botocore.client.EMR
            session boto3 EMR
        cluster_id : str
            cluster identifier string value

        Returns
        -------
        int
            0 if the cluster is WAITING state, and system exit for termination
            raises an exception if runs into termination
        """
        cluster_status = "STARTING"

        while cluster_status not in (
            "WAITING",
            "TERMINATING",
            "TERMINATED",
            "TERMINATED_WITH_ERRORS",
        ):
            get_cluster_status = session.describe_cluster(ClusterId=cluster_id)
            cluster_status = get_cluster_status["Cluster"]["Status"]["State"]
            state_change_reason = get_cluster_status["Cluster"]["Status"][
                "StateChangeReason"
            ]

            time.sleep(30)
        if cluster_status in ("TERMINATING", "TERMINATED", "TERMINATED_WITH_ERRORS"):
            raise Exception(f"Cluster terminated with errors \n {state_change_reason}")
            sys.exit(1)

        print("Cluster is up and running, please proceed")
        return 0

    def terminate_emr_cluster(
        self, session: "botocore.client.EMR", cluster_id: str
    ) -> int:
        """
        terminate created cluster

        Parameters
        ----------
        session : botocore.client.EMR
            session boto3 EMR
        cluster_id : str
            cluster identifier string value

        Returns
        -------
        int
            0 if the cluster is terminated
        """
        session.terminate_job_flows(JobFlowIds=[cluster_id])
        return 0

    def get_cluster_id(
        self, session: "botocore.client.EMR", task_id: str, identifier: str
    ) -> str:
        """
        fetch cluster identifier string value

        Parameters
        ----------
        session : botocore.client.EMR
            session boto3 EMR
        task_id: str
            task identifier from airflow
        identifier: str
            date identifier from airflow

        Returns
        -------
        str
            cluster identifier string value
        """
        all_clusters = session.list_clusters(
            ClusterStates=[
                "WAITING",
            ],
        )["Clusters"]
        cluster_id = "test"

        for i in all_clusters:
            if (i["Status"]["State"] == "WAITING") and (
                i["Name"] == f"churn__{task_id}__{identifier}"
            ):
                cluster_id = i["Id"]

        return cluster_id

    def get_emr_master_dns_name(
        self, session: "botocore.client.EMR", cluster_id: str
    ) -> str:
        """
        fetch cluster master node dns address

        Parameters
        ----------
        session : botocore.client.EMR
            session boto3 EMR
        cluster_id : str
            cluster identifier string value

        Returns
        -------
        str
            cluster master node dns address
        """
        dns_name = session.describe_cluster(ClusterId=cluster_id)["Cluster"][
            "MasterPublicDnsName"
        ]

        return dns_name

    def spin_up_emr_cluster(
        self,
        session: "botocore.client.EMR",
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str,
    ) -> int:
        """
        fetch cluster master node dns address

        Parameters
        ----------
        session : botocore.client.EMR
            session of EMR
        master_instance_type: str
            master instance type
        core_instance_type: str
            core instance type
        core_instance_count: int
            number of core instances
        configurations: List
            configurations of creating cluster
        applications: List
            applications that should be created for the cluster
        log_uri: str
            s3 directory of logs
        task_id: str
            airflow task id
        identifier: str
            identifier date
        bidprice: str
            bidprice of spot instances

        Returns
        -------
        0
            raises an exception if the cluster does not exist
        """
        create_loop = 1
        max_tries = 1

        while (create_loop == 1) and (max_tries < 4):
            response = self.create_emr_cluster(
                session=session,
                master_instance_type=master_instance_type,
                core_instance_type=core_instance_type,
                core_instance_count=core_instance_count,
                configurations=configurations,
                applications=applications,
                log_uri=log_uri,
                task_id=task_id,
                identifier=identifier,
                bidprice=bidprice,
            )

            # sleep for 3.5 minutes before checking
            time.sleep(210)

            # get all results
            try:
                ip_address = self.get_emr_master_dns_name(
                    session=session, cluster_id=response["JobFlowId"]
                ).split("-")[1]
            except Exception:
                ip_address = "3"

            if len(ip_address) == 1:
                # terminate cluster
                self.terminate_emr_cluster(
                    session=session, cluster_id=response["JobFlowId"]
                )
                max_tries += 1
                continue
            create_loop = 0

        # check created cluster in waiting state
        cluster_response = self.check_emr_cluster_status(
            session=session,
            cluster_id=response["JobFlowId"],
        )
        if cluster_response:
            raise Exception(f"cluster does not exist: churn__{task_id}__{identifier}")

        return 0
