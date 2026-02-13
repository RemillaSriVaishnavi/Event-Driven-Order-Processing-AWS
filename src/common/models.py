import json


def insert_order(cursor, order_id, customer_id, items):
    cursor.execute(
        "INSERT INTO orders (order_id, customer_id, items, status) VALUES (%s, %s, %s, 'PENDING')",
        (order_id, customer_id, json.dumps(items))
    )


def update_order_status(cursor, order_id, status):
    cursor.execute(
        "UPDATE orders SET status=%s WHERE order_id=%s",
        (status, order_id)
    )


def update_order_processed(cursor, order_id, processed_at):
    cursor.execute(
        "UPDATE orders SET status='PROCESSED', processed_at=%s WHERE order_id=%s",
        (processed_at, order_id)
    )


def check_inventory(cursor, product_id, quantity):
    cursor.execute(
        "SELECT quantity_available FROM inventory WHERE product_id = %s FOR UPDATE",
        (product_id,)
    )
    result = cursor.fetchone()

    if not result or result[0] < quantity:
        return False
    return True


def decrement_inventory(cursor, product_id, quantity):
    cursor.execute(
        "UPDATE inventory SET quantity_available = quantity_available - %s WHERE product_id = %s",
        (quantity, product_id)
    )
