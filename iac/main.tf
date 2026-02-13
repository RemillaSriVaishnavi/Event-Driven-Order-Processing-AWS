provider "aws" {
  region = var.aws_region
}

# SQS Queues
resource "aws_sqs_queue" "order_created" {
  name = "order-created-queue"
}

resource "aws_sqs_queue" "order_created_dlq" {
  name = "order-created-dlq"
}

resource "aws_sqs_queue_redrive_policy" "redrive" {
  queue_url = aws_sqs_queue.order_created.id

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_created_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "order_processed" {
  name = "order-processed-queue"
}

# IAM Role for Lambdas
resource "aws_iam_role" "lambda_role" {
  name = "order-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "sqs:*",
        "logs:*"
      ],
      Resource = "*"
    }]
  })
}
