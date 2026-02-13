resource "aws_sqs_queue" "order_created_dlq" {
  name = "order-created-dlq"
}

resource "aws_sqs_queue" "order_created_queue" {
  name = "order-created-queue"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_created_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "order_processed_queue" {
  name = "order-processed-queue"
}
