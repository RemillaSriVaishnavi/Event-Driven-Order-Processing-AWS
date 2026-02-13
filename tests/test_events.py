import json
from unittest.mock import patch
from src.common.sqs_publisher import publish_order_processed


@patch("src.common.sqs_publisher.sqs")
def test_publish_order_processed(mock_sqs):

    event = {
        "order_id": "test-1",
        "customer_id": "cust-1",
        "status": "PROCESSED",
        "processed_at": "2026-01-01T00:00:00Z"
    }

    publish_order_processed(event)

    mock_sqs.send_message.assert_called_once()

    args, kwargs = mock_sqs.send_message.call_args
    sent_body = json.loads(kwargs["MessageBody"])

    assert sent_body["order_id"] == "test-1"
    assert sent_body["status"] == "PROCESSED"
