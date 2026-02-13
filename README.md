# Event-Driven Order Processing System (AWS)

## Overview

This project implements a **robust, scalable event-driven backend system** for processing e-commerce orders using **AWS serverless services**.

The system follows **Event-Driven Architecture (EDA)** principles, where orders are processed asynchronously using message queues and decoupled serverless functions.

The implementation demonstrates:

* API Gateway integration
* Asynchronous messaging using Amazon SQS
* Serverless processing with AWS Lambda
* Transactional inventory management with MySQL (RDS)
* Dead Letter Queue (DLQ) handling
* Infrastructure as Code (Terraform)
* Unit testing with ≥70% coverage of business logic
* Local development using Docker


## Architecture Overview

## Event Flow

```
Client
  ↓
API Gateway (POST /api/orders)
  ↓
CreateOrder Lambda
  ↓
OrderCreated SQS Queue
  ↓
OrderProcessor Lambda
  ↓
MySQL (orders + inventory tables)
  ↓
OrderProcessed SQS Queue
  ↓
NotificationSender Lambda
  ↓
CloudWatch Logs
```


## AWS Services Used

| Component          | AWS Service        |
| ------------------ | ------------------ |
| API Layer          | Amazon API Gateway |
| Messaging          | Amazon SQS         |
| Dead Letter Queue  | Amazon SQS DLQ     |
| Serverless Compute | AWS Lambda         |
| Database           | Amazon RDS (MySQL) |
| Monitoring         | Amazon CloudWatch  |
| Infrastructure     | Terraform          |



## Project Structure

```
event-driven-order-processing/
│
├── db/
│   ├── schema.sql
│   └── seed.sql
│
├── iac/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── iam.tf
│   ├── api_gateway.tf
│   ├── lambda.tf
│   ├── rds.tf
│   └── sqs.tf
│
├── src/
│   │
│   ├── api/ 
│   │   └── create_order.py
│   │
│   ├── common/
│   │   ├── db.py
│   │   ├── idempotency.py
│   │   ├── models.py
│   │   ├── sqs_client.py
│   │   └── sqs_publisher.py
│   │
│   ├── notification_sender/
│   │   └── handler.py
│   │
│   └── order_processor/
│       └── handler.py
│
├── tests/
│   ├── test_events.py
│   ├── test_inventory.py
│   └── test_order_processor.py
│
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore

```


## Database Schema

## Orders Table

```sql
CREATE TABLE orders (
  order_id VARCHAR(36) PRIMARY KEY,
  customer_id VARCHAR(255) NOT NULL,
  items JSON NOT NULL,
  status ENUM('PENDING','PROCESSED','FAILED') NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  processed_at DATETIME NULL
);
```

## Inventory Table

```sql
CREATE TABLE inventory (
  product_id VARCHAR(255) PRIMARY KEY,
  product_name VARCHAR(255),
  quantity_available INT NOT NULL
);
```

Inventory is pre-seeded with sample products.


## API Endpoint

### POST `/api/orders`

#### Request Body

```json
{
  "customer_id": "cust-101",
  "items": [
    { "product_id": "prod-1", "quantity": 2 }
  ]
}
```

#### Responses

| Scenario        | Status Code     |
| --------------- | --------------- |
| Valid request   | 202 Accepted    |
| Invalid request | 400 Bad Request |



## Event Schemas

### OrderCreated Event

```json
{
  "order_id": "uuid",
  "customer_id": "cust-101",
  "items": [
    { "product_id": "prod-1", "quantity": 2 }
  ],
  "timestamp": "2026-02-09T10:00:00Z"
}
```

### OrderProcessed Event

```json
{
  "order_id": "uuid",
  "customer_id": "cust-101",
  "status": "PROCESSED",
  "processed_at": "2026-02-09T10:01:00Z"
}
```


## Order Processing Logic

Inside `OrderProcessor` Lambda:

1. Start DB transaction
2. Insert order as `PENDING`
3. Lock inventory rows (`SELECT ... FOR UPDATE`)
4. Validate available stock
5. Decrement inventory
6. Update order status:

   * `PROCESSED` if success
   * `FAILED` if insufficient inventory
7. Commit or rollback
8. Publish `OrderProcessed` event



## Dead Letter Queue (DLQ)

* `order-created-dlq`
* Attached to `order-created-queue`
* `maxReceiveCount = 3`
* Failed messages automatically moved to DLQ


## Security & IAM

* Least privilege IAM roles
* Lambdas only allowed required SQS actions
* No hardcoded credentials
* DB credentials stored in environment variables


## Infrastructure as Code (Terraform)

All AWS resources are defined in the `iac/` directory:

* SQS queues
* DLQ
* IAM roles
* Lambda roles
* API Gateway (if extended)
* RDS (if extended)

## Deploy Infrastructure

```bash
cd iac
terraform init
terraform apply
```


## Local Development

Run MySQL + Tests locally:

```bash
docker-compose up --build
```

This:

* Starts MySQL
* Loads schema + seed data
* Runs unit tests


## Unit Testing

Unit tests focus on:

* Inventory validation
* Order status transitions
* Event publishing logic
* Failure scenarios

To run locally:

```bash
pytest
```

Target coverage: **≥70% of OrderProcessor logic**



## Failure Handling

| Scenario               | Outcome              |
| ---------------------- | -------------------- |
| Invalid input          | 400 returned         |
| DB failure             | Transaction rollback |
| Insufficient inventory | Order marked FAILED  |
| Multiple failures      | Message moved to DLQ |



## Design Decisions

### Why Event-Driven?

* Loose coupling
* High scalability
* Failure isolation
* Independent service evolution

### Why SQS?
* Fully managed
* At-least-once delivery
* DLQ support

### Why Transactions?

* Prevent partial inventory updates
* Ensure data consistency


## Deployment Steps (AWS Console)

1. Create SQS queues
2. Configure DLQ
3. Create RDS MySQL instance
4. Create Lambdas
5. Attach SQS triggers
6. Configure API Gateway
7. Set environment variables
8. Deploy


## Conclusion

This project demonstrates a **production-ready serverless event-driven backend** on AWS that:

* Scales automatically
* Handles failures gracefully
* Maintains data consistency
* Follows cloud-native best practices

It simulates a real-world e-commerce order processing pipeline using modern backend architecture principles.

