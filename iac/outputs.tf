output "order_created_queue_url" {
  value = aws_sqs_queue.order_created_queue.id
}

output "order_processed_queue_url" {
  value = aws_sqs_queue.order_processed_queue.id
}

output "db_endpoint" {
  value = aws_db_instance.order_db.endpoint
}
