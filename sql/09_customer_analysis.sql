
-- CUSTOMER PURCHASE BEHAVIOR

USE ecommerce_analytics;

-- Create a reusable customer-level summary
-- One row represents one unique customer

CREATE OR REPLACE VIEW customer_purchase_summary AS
SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_spent,
    MIN(order_purchase_timestamp) AS first_purchase,
    MAX(order_purchase_timestamp) AS last_purchase
FROM ecommerce_sales
GROUP BY customer_unique_id;


-- 1. Total unique customers
SELECT
    COUNT(*) AS total_customers
FROM customer_purchase_summary;


-- 2. One-time vs repeat customers
SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END AS customer_type,
    COUNT(*) AS total_customers
FROM customer_purchase_summary
GROUP BY customer_type;


-- 3. Repeat customer percentage
SELECT
    COUNT(*) AS total_customers,
    SUM(
        CASE WHEN total_orders > 1
        THEN 1 ELSE 0 END
    ) AS repeat_customers,
    ROUND(
        100.0 * SUM(
            CASE WHEN total_orders > 1
            THEN 1 ELSE 0 END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage
FROM customer_purchase_summary;


-- 4. Customer purchase frequency distribution
SELECT
    total_orders AS number_of_purchases,
    COUNT(*) AS number_of_customers
FROM customer_purchase_summary
GROUP BY total_orders
ORDER BY total_orders;


-- 5. Top 10 customers by spending
SELECT
    customer_unique_id,
    total_orders,
    total_spent,
    first_purchase,
    last_purchase
FROM customer_purchase_summary
ORDER BY total_spent DESC
LIMIT 10;


-- 6. Average customer spending
SELECT
    ROUND(AVG(total_spent), 2) AS avg_customer_spending,
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer
FROM customer_purchase_summary;


-- 7. Revenue from one-time vs repeat customers
SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(SUM(total_spent), 2) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_customer_spending
FROM customer_purchase_summary
GROUP BY customer_type;
