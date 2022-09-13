import os
import time
import uuid

import boto3


kinesis = boto3.client('kinesis', region_name=os.environ['AWS_REGION'])


def stream_ready():
  try:
    response = kinesis.describe_stream(StreamName=os.environ['STREAM_NAME'])
    if response['StreamDescription']['StreamStatus'] == 'ACTIVE':
      response = kinesis.put_record(StreamName=os.environ['STREAM_NAME'],
                        Data="INFO Test message".encode("utf-8"),
                        PartitionKey="1")
      print("test message publish response")
      print(response)
      return 'SequenceNumber' in response
  except:
    pass
  return False


def on_event(event, context):
  print(event)
  is_create_update = event['RequestType'] in ['Create', 'Update']

  if is_create_update:
    while not stream_ready():
      time.sleep(30)
    return event.get('PhysicalResourceId', str(uuid.uuid4()))

