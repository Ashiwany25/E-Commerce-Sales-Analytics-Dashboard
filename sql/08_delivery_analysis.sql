
-- DELIVERY PERFORMANCE ANALYSIS

USE ecommerce_analytics;

-- One order may contain multiple products.
-- Create an order-level view to avoid double counting.

CREATE OR REPLACE VIEW order_delivery_summary AS
SELECT
    order_id,
    MAX(customer_state) AS customer_state,
    MAX(order_purchase_timestamp) AS purchase_date,
    MAX(order_delivered_customer_date) AS delivery_date,
    MAX(order_estimated_delivery_date) AS estimated_date,
    MAX(delivery_days) AS delivery_days
FROM ecommerce_sales
GROUP BY order_id;


-- 1. Overall delivery performance
SELECT
    COUNT(*) AS total_orders,
    COUNT(delivery_days) AS orders_with_delivery_time,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(MIN(delivery_days), 2) AS fastest_delivery_days,
    ROUND(MAX(delivery_days), 2) AS slowest_delivery_days
FROM order_delivery_summary;


-- 2. On-time vs late deliveries
-- Compare calendar dates, not times of day.
SELECT
    COUNT(*) AS total_deliveries,
    SUM(
        CASE
            WHEN DATE(delivery_date) > DATE(estimated_date)
            THEN 1 ELSE 0
        END
    ) AS late_deliveries,
    SUM(
        CASE
            WHEN DATE(delivery_date) <= DATE(estimated_date)
            THEN 1 ELSE 0
        END
    ) AS on_time_deliveries
FROM order_delivery_summary
WHERE delivery_date IS NOT NULL
  AND estimated_date IS NOT NULL;


-- 3. Late delivery percentage
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN DATE(delivery_date) > DATE(estimated_date)
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage
FROM order_delivery_summary
WHERE delivery_date IS NOT NULL
  AND estimated_date IS NOT NULL;


-- 4. Average delivery time by state
SELECT
    customer_state,
    COUNT(*) AS total_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days
FROM order_delivery_summary
GROUP BY customer_state
ORDER BY avg_delivery_days DESC;


-- 5. Top 10 states with highest late delivery rates
SELECT
    customer_state,
    COUNT(*) AS total_deliveries,
    SUM(
        CASE
            WHEN DATE(delivery_date) > DATE(estimated_date)
            THEN 1 ELSE 0
        END
    ) AS late_deliveries,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN DATE(delivery_date) > DATE(estimated_date)
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage
FROM order_delivery_summary
WHERE delivery_date IS NOT NULL
  AND estimated_date IS NOT NULL
GROUP BY customer_state
ORDER BY late_delivery_percentage DESC
LIMIT 10;
