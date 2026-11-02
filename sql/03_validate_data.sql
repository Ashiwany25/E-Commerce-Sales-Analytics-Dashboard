
-- VALIDATE IMPORTED E-COMMERCE DATA

USE ecommerce_analytics;

-- 1. Check total records
SELECT COUNT(*) AS total_records
FROM ecommerce_sales;

-- 2. Count unique orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales;

-- 3. Count unique customers
SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
FROM ecommerce_sales;

-- 4. Calculate total revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales;

-- 5. Check missing prices
SELECT COUNT(*) AS missing_prices
FROM ecommerce_sales
WHERE price IS NULL;

-- 6. Check duplicate order-item combinations
SELECT order_id, order_item_id, COUNT(*) AS duplicate_count
FROM ecommerce_sales
GROUP BY order_id, order_item_id
HAVING COUNT(*) > 1;

-- 7. Check order statuses
SELECT order_status, COUNT(*) AS total_records
FROM ecommerce_sales
GROUP BY order_status;

-- 8. Check negative revenue
SELECT COUNT(*) AS negative_revenue_records
FROM ecommerce_sales
WHERE revenue < 0;

-- 9. Display first five records
SELECT *
FROM ecommerce_sales
LIMIT 5;
