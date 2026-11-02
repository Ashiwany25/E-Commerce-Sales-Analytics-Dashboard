
-- E-COMMERCE BUSINESS KPIs

USE ecommerce_analytics;

-- 1. Total revenue
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales;

-- 2. Total unique orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales;

-- 3. Total unique customers
SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM ecommerce_sales;

-- 4. Average Order Value (AOV)
SELECT
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM ecommerce_sales;

-- 5. Total products sold
SELECT
    COUNT(*) AS total_products_sold
FROM ecommerce_sales;

-- 6. Combined KPI report
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value,
    COUNT(*) AS total_products_sold
FROM ecommerce_sales;
