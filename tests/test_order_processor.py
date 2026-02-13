from unittest.mock import patch
from src.order_processor.handler import lambda_handler


@patch("src.order_processor.handler.order_already_processed", return_value=False)
@patch("src.order_processor.handler.get_connection")
@patch("src.order_processor.handler.publish_order_processed")
def test_order_processing_success(mock_publish, mock_conn, mock_idem):

    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (10,)

    event = {
        "Records": [{
            "body": '{"order_id":"1","customer_id":"c1","items":[{"product_id":"prod-1","quantity":1}]}'
        }]
    }

    lambda_handler(event, None)

    assert mock_publish.called


@patch("src.order_processor.handler.order_already_processed", return_value=True)
def test_duplicate_order(mock_idem):

    event = {
        "Records": [{
            "body": '{"order_id":"1","customer_id":"c1","items":[{"product_id":"prod-1","quantity":1}]}'
        }]
    }

    lambda_handler(event, None)
