CREATE TABLE orders (
  order_id VARCHAR(36) PRIMARY KEY,
  customer_id VARCHAR(255) NOT NULL,
  items JSON NOT NULL,
  status ENUM('PENDING','PROCESSED','FAILED') NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  processed_at DATETIME NULL
);

CREATE TABLE inventory (
  product_id VARCHAR(255) PRIMARY KEY,
  product_name VARCHAR(255),
  quantity_available INT NOT NULL
);
