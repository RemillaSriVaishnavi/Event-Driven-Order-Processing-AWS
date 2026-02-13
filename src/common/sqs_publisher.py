import boto3
import json
import os

sqs = boto3.client("sqs", region_name=os.environ["AWS_REGION"])

ORDER_PROCESSED_QUEUE_URL = os.environ["ORDER_PROCESSED_QUEUE_URL"]

def publish_order_processed(event):
    sqs.send_message(
        QueueUrl=ORDER_PROCESSED_QUEUE_URL,
        MessageBody=json.dumps(event)
    )
