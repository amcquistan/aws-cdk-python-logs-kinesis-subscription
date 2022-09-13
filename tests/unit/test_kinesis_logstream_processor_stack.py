import aws_cdk as core
import aws_cdk.assertions as assertions

from kinesis_logstream_processor.stack import KinesisLogstreamProcessorStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kinesis_logstream_processor/kinesis_logstream_processor_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KinesisLogstreamProcessorStack(app, "kinesis-logstream-processor")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
