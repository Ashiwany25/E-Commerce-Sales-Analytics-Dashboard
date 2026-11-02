
-- MONTHLY SALES ANALYSIS

USE ecommerce_analytics;

-- 1. Monthly revenue
SELECT
    DATE_FORMAT(
        order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY sales_month
ORDER BY sales_month;


-- 2. Monthly unique orders
SELECT
    DATE_FORMAT(
        order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales
GROUP BY sales_month
ORDER BY sales_month;


-- 3. Monthly average order value
SELECT
    DATE_FORMAT(
        order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM ecommerce_sales
GROUP BY sales_month
ORDER BY sales_month;


-- 4. Combined monthly sales report
SELECT
    DATE_FORMAT(
        order_purchase_timestamp, '%Y-%m'
    ) AS sales_month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value,
    COUNT(*) AS total_items_sold
FROM ecommerce_sales
GROUP BY sales_month
ORDER BY sales_month;

