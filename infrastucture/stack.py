from aws_cdk import (
  aws_ecs as ecs,
  aws_ec2 as ec2,
  CfnOutput,
  Stack,
)
from constructs import Construct


class InfrastructureStack(Stack):
  vpc: ec2.Vpc
  fargate_cluster: ecs.Cluster

  def __init__(self, scope: Construct, construct_id: str, **kwargs):
    super().__init__(scope, construct_id, **kwargs)
    self.vpc = ec2.Vpc(self, "vpc", max_azs=2, nat_gateways=0)
    self.fargate_cluster = ecs.Cluster(self, "fargate-cluster", vpc=self.vpc)

    CfnOutput(self, "vpcid", value=self.vpc.vpc_id)
    CfnOutput(self, "fargate-cluster-arn", value=self.fargate_cluster.cluster_arn)
