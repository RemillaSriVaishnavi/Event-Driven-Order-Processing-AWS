import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        order_id = body["order_id"]
        customer_id = body["customer_id"]

        logger.info(
            f"Notification sent for Order ID: {order_id} to Customer ID: {customer_id}"
        )
