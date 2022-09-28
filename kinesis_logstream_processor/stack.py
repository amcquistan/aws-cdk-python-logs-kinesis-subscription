from pathlib import Path

from aws_cdk import (
  aws_ecs as ecs,
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_kinesis as kinesis,
  aws_lambda as lambda_,
  aws_logs as logs,
  aws_logs_destinations as logs_dest,
  CustomResource,
  custom_resources as cr,
  Duration,
  Stack,
)
from constructs import Construct


class KinesisLogStreamProcessorStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, log_group: logs.LogGroup, stream: kinesis.Stream, **kwargs):
    super().__init__(scope, construct_id, **kwargs)

    status_fn = lambda_.Function(self, "status-fn",
      code=lambda_.Code.from_asset(str(Path(__file__).parent.joinpath("functions"))),
      runtime=lambda_.Runtime.PYTHON_3_9,
      handler="kinesis_status.on_event",
      timeout=Duration.minutes(12),
      environment={
        "STREAM_NAME": stream.stream_name
      }
    )

    stream.grant(status_fn, "*")

    provider = cr.Provider(self, "stream-status-provider",
      on_event_handler=status_fn,
      log_retention=logs.RetentionDays.THREE_DAYS
    )

    custom_resource = CustomResource(self, "stream-status-resource",
      resource_type="Custom::KinesisStatusChecker",
      service_token=provider.service_token
    )

    destination = logs_dest.KinesisDestination(stream)

    filter = logs.SubscriptionFilter(self, "applog-filter",
      log_group=log_group,
      destination=destination,
      filter_pattern=logs.FilterPattern.all_events()
    )
    filter.node.add_dependency(custom_resource)
