from common.db import get_connection


def order_already_processed(order_id: str) -> bool:
    """
    Checks if order already exists in DB.
    Prevents duplicate inventory updates.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM orders WHERE order_id = %s",
        (order_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return True
    return False
