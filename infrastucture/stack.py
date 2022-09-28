from aws_cdk import (
  aws_ecs as ecs,
  aws_ec2 as ec2,
  aws_kinesis as kinesis,
  CfnOutput,
  Stack,
)
from constructs import Construct


class InfrastructureStack(Stack):
  vpc: ec2.Vpc
  fargate_cluster: ecs.Cluster
  kinesis_stream: kinesis.Stream

  def __init__(self, scope: Construct, construct_id: str, **kwargs):
    super().__init__(scope, construct_id, **kwargs)
    self.vpc = ec2.Vpc(self, "vpc", max_azs=2, nat_gateways=0)
    self.fargate_cluster = ecs.Cluster(self, "fargate-cluster", vpc=self.vpc)

    self.kinesis_stream = kinesis.Stream(self, "logstream", stream_name="loggingapp-stream", shard_count=2)

    CfnOutput(self, "vpcid", value=self.vpc.vpc_id)
    CfnOutput(self, "fargate-cluster-arn", value=self.fargate_cluster.cluster_arn)
