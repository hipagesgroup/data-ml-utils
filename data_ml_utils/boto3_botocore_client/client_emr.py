import time
from typing import List

import polling
import requests

from data_ml_utils.boto3_botocore_client.client_initialisation import AwsClients


class AwsEMRServices:
    """
    Class that handles all aws related services
    This includes creating of EMR cluster, terminating cluster,
    retrieving status and ip address of cluster
    Initialisation of class returns the boto3 session and emr client
    """

    def __init__(self):
        client_class = AwsClients()
        self.client_emr = client_class.client_emr

    def create_emr_cluster(
        self,
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str,
        emr_version: str,
    ) -> dict:
        """
        creates EMR cluster

        Parameters
        ----------
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
        emr_version: str
            version of EMR, emr-6.7.0

        Returns
        -------
        dict
            response of request of creating cluster, raises exception if not successful
        """
        response = self.client_emr.run_job_flow(
            Name=f"churn__{task_id}__{identifier}",
            LogUri=log_uri,
            ReleaseLabel=emr_version,
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
                                "TimeoutDurationMinutes": 5,
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
            ServiceRole="EMR_DefaultRole",
            VisibleToAllUsers=True,
            ScaleDownBehavior="TERMINATE_AT_TASK_COMPLETION",
            ManagedScalingPolicy={
                "ComputeLimits": {
                    "UnitType": "InstanceFleetUnits",
                    "MinimumCapacityUnits": 60,
                    "MaximumCapacityUnits": 120,
                    "MaximumOnDemandCapacityUnits": 0,
                    "MaximumCoreCapacityUnits": 120,
                }
            },
            AutoTerminationPolicy={"IdleTimeout": 1200},
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(
                f"Encountered Error while Launching the EMR Cluster \n {response}"
            )

        return response

    def check_emr_cluster_status(self, cluster_id: str) -> int:
        """
        check emr cluster that is created
        raises exception if the cluster runs into termination issues

        Parameters
        ----------
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
            get_cluster_status = self.client_emr.describe_cluster(ClusterId=cluster_id)
            cluster_status = get_cluster_status["Cluster"]["Status"]["State"]
            state_change_reason = get_cluster_status["Cluster"]["Status"][
                "StateChangeReason"
            ]

            time.sleep(30)
        if cluster_status in ("TERMINATING", "TERMINATED", "TERMINATED_WITH_ERRORS"):
            raise Exception(f"Cluster terminated with errors \n {state_change_reason}")

        print("Cluster is up and running, please proceed")
        return 0

    def terminate_emr_cluster(self, cluster_id: str) -> int:
        """
        terminate created cluster

        Parameters
        ----------
        cluster_id : str
            cluster identifier string value

        Returns
        -------
        int
            0 if the cluster is terminated
        """
        self.client_emr.terminate_job_flows(JobFlowIds=[cluster_id])
        return 0

    def get_cluster_id(self, task_id: str, identifier: str) -> str:
        """
        fetch cluster identifier string value

        Parameters
        ----------
        task_id: str
            task identifier from airflow
        identifier: str
            date identifier from airflow

        Returns
        -------
        str
            cluster identifier string value
        """
        all_clusters = self.client_emr.list_clusters(
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

    def get_emr_master_dns_name(self, cluster_id: str) -> str:
        """
        fetch cluster master node dns address

        Parameters
        ----------
        cluster_id : str
            cluster identifier string value

        Returns
        -------
        str
            cluster master node dns address
        """
        dns_name = self.client_emr.describe_cluster(ClusterId=cluster_id)["Cluster"][
            "MasterPublicDnsName"
        ]

        return dns_name

    def get_dns_status(self, response_body: dict) -> bool:
        """
        check if EMR cluster has an master DNS address

        Parameters
        ----------
        response_body: dict
            task identifier from airflow

        Returns
        -------
        bool
            boolean if EMR cluster has an master DNS address
        """
        if response_body.get("MasterPublicDnsName") is None:
            return False
        return True

    def spin_up_emr_cluster(
        self,
        master_instance_type: str,
        core_instance_type: str,
        core_instance_count: int,
        configurations: List,
        applications: List,
        log_uri: str,
        task_id: str,
        identifier: str,
        bidprice: str,
        emr_version: str,
    ) -> int:
        """
        fetch cluster master node dns address

        Parameters
        ----------
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
        emr_version: str
            version of EMR, emr-6.7.0

        Returns
        -------
        0
            raises an exception if the cluster does not exist
        """
        max_tries = 1

        while max_tries < 4:
            response = self.create_emr_cluster(
                master_instance_type=master_instance_type,
                core_instance_type=core_instance_type,
                core_instance_count=core_instance_count,
                configurations=configurations,
                applications=applications,
                log_uri=log_uri,
                task_id=task_id,
                identifier=identifier,
                bidprice=bidprice,
                emr_version=emr_version,
            )

            # poll get emr master dns name every 30 seconds
            polling_response = polling.poll(
                lambda: self.get_dns_status(
                    self.client_emr.describe_cluster(ClusterId=response["JobFlowId"])[
                        "Cluster"
                    ]
                ),
                step=15,
                ignore_exceptions=(requests.exceptions.ConnectionError,),
                poll_forever=False,
                timeout=330,
            )

            # logic of checking if address is valid
            try:
                ip_address = self.get_emr_master_dns_name(
                    cluster_id=response["JobFlowId"]
                ).split("-")[1]
            except Exception:
                ip_address = "3"

            if (len(ip_address) == 1) | (not polling_response):
                # terminate cluster
                self.terminate_emr_cluster(cluster_id=response["JobFlowId"])
                max_tries += 1
                continue
            break

        # check created cluster in waiting state
        cluster_response = self.check_emr_cluster_status(
            cluster_id=response["JobFlowId"],
        )
        if cluster_response:
            raise Exception(f"cluster does not exist: churn__{task_id}__{identifier}")

        return 0
