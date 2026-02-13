import json
import uuid
from datetime import datetime
from common.sqs_client import publish_order_created


def validate_request(body: dict):
    """
    Validates incoming order payload
    """
    if "customer_id" not in body:
        return False, "customer_id is required"

    if "items" not in body or not isinstance(body["items"], list):
        return False, "items must be a list"

    if len(body["items"]) == 0:
        return False, "items cannot be empty"

    for item in body["items"]:
        if "product_id" not in item:
            return False, "product_id missing in item"
        if "quantity" not in item:
            return False, "quantity missing in item"
        if item["quantity"] <= 0:
            return False, "quantity must be greater than 0"

    return True, None


def lambda_handler(event, context):
    # Parse JSON body
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format"})
        }

    # Validate input
    is_valid, error = validate_request(body)
    if not is_valid:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": error})
        }

    # Create OrderCreated event
    order_event = {
        "order_id": str(uuid.uuid4()),
        "customer_id": body["customer_id"],
        "items": body["items"],
        "timestamp": datetime.utcnow().isoformat()
    }

    # Publish event to SQS
    publish_order_created(order_event)

    # Return 202 Accepted
    return {
        "statusCode": 202,
        "body": json.dumps({
            "message": "Order accepted",
            "order_id": order_event["order_id"]
        })
    }
