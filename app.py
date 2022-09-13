#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastucture.stack import InfrastructureStack
from kinesis_logstream_processor.stack import KinesisLogStreamProcessorStack
from logging_datagen.stack import LoggingDatagenStack


app = cdk.App()
env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

infra_stack = InfrastructureStack(app, "infrastructure-stack",
  env=env,
  stack_name="log-processor-infrastructure"
)

logging_datagen_stack = LoggingDatagenStack(app, "loggingdatagen-stack",
  env=env,
  stack_name="logging-datagen",
  vpc=infra_stack.vpc,
  fargate_cluster=infra_stack.fargate_cluster
)

KinesisLogStreamProcessorStack(app, "stream-processor",
  env=env,
  stack_name="stream-processor",
  log_group=logging_datagen_stack.log_group
)

app.synth()
