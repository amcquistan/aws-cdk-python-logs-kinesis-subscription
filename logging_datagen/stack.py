from pathlib import Path

from aws_cdk import (
  aws_ecs as ecs,
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_logs as logs,
  CfnOutput,
  Stack,
)
from constructs import Construct


class LoggingDatagenStack(Stack):
  log_group: logs.LogGroup

  def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, fargate_cluster: ecs.Cluster, **kwargs):
    super().__init__(scope, construct_id, **kwargs)

    task_def = ecs.FargateTaskDefinition(self, "taskdef",
      execution_role=iam.Role(self, "exec-role",
        assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        role_name="logging-app-task-exec-role",
        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")]
    ))
    self.log_group = logs.LogGroup(self, "loggroup", log_group_name="loggingdatagen", retention=logs.RetentionDays.THREE_DAYS)
    task_def.add_container("app-container",
      logging=ecs.LogDriver.aws_logs(
        stream_prefix="app-container",
        log_group=self.log_group
      ),
      image=ecs.ContainerImage.from_asset(
        directory=str(Path(__file__).resolve().parent.joinpath("logging_app"))
      ),
      essential=True,
      health_check=ecs.HealthCheck(command=["CMD-SHELL", "pgrep -f loggingdatagen || exit 1"])
    )

    ecs.FargateService(self, "fargate-svc",
      service_name="logging-datagen",
      cluster=fargate_cluster,
      task_definition=task_def,
      vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
      assign_public_ip=True
    )