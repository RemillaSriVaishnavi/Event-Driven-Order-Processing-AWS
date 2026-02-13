import json
from datetime import datetime
from common.db import get_connection
from common.models import insert_order, update_order_processed, update_order_status, check_inventory, decrement_inventory
from common.idempotency import order_already_processed
from common.sqs_publisher import publish_order_processed


def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        order_id = body["order_id"]
        customer_id = body["customer_id"]
        items = body["items"]

        if order_already_processed(order_id):
            print(f"Duplicate order detected: {order_id}")
            continue

        conn = get_connection()
        cursor = conn.cursor()

        try:
            insert_order(cursor, order_id, customer_id, items)

            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]

                if not check_inventory(cursor, product_id, quantity):
                    raise Exception("Insufficient inventory")

                decrement_inventory(cursor, product_id, quantity)

            update_order_processed(cursor, order_id, datetime.utcnow())

            conn.commit()

            publish_order_processed({
                "order_id": order_id,
                "customer_id": customer_id,
                "status": "PROCESSED",
                "processed_at": datetime.utcnow().isoformat()
            })

        except Exception as e:
            conn.rollback()
            update_order_status(cursor, order_id, "FAILED")
            conn.commit()
            raise e

        finally:
            cursor.close()
            conn.close()
