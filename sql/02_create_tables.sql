
USE ecommerce_analytics;

CREATE TABLE IF NOT EXISTS ecommerce_sales (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10),
    product_id VARCHAR(50),
    product_category_name VARCHAR(150),
    seller_id VARCHAR(50),
    price DECIMAL(12,2),
    freight_value DECIMAL(12,2),
    revenue DECIMAL(12,2),
    order_year INT,
    order_month INT,
    order_day INT,
    delivery_days DECIMAL(10,2),

    PRIMARY KEY (order_id, order_item_id),

    INDEX idx_order_date (order_purchase_timestamp),
    INDEX idx_customer (customer_unique_id),
    INDEX idx_category (product_category_name),
    INDEX idx_state (customer_state)
);
