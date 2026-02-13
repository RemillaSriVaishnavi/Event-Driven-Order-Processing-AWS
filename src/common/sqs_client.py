import boto3
import json
import os

# Create SQS client
sqs = boto3.client(
    "sqs",
    region_name=os.environ.get("AWS_REGION")
)

QUEUE_URL = os.environ.get("ORDER_CREATED_QUEUE_URL")


def publish_order_created(event: dict):
    """
    Publishes OrderCreated event to SQS
    """
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(event)
    )
    return response
