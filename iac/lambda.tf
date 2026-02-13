resource "aws_lambda_function" "order_processor" {
  function_name = "order-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.10"
  filename      = "lambda.zip"

  environment {
    variables = {
      AWS_REGION                = var.aws_region
      DB_HOST                   = aws_db_instance.order_db.endpoint
      DB_USER                   = var.db_username
      DB_PASSWORD               = var.db_password
      DB_NAME                   = var.db_name
      ORDER_PROCESSED_QUEUE_URL = aws_sqs_queue.order_processed_queue.id
    }
  }
}
