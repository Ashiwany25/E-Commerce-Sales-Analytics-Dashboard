
-- STATE-WISE SALES ANALYSIS

USE ecommerce_analytics;

-- 1. Top 10 states by revenue
SELECT
    customer_state,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM ecommerce_sales
GROUP BY customer_state
ORDER BY total_revenue DESC
LIMIT 10;


-- 2. Top 10 states by order volume
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY customer_state
ORDER BY total_orders DESC
LIMIT 10;


-- 3. Average Order Value by state
SELECT
    customer_state,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM ecommerce_sales
GROUP BY customer_state
ORDER BY average_order_value DESC;


-- 4. Revenue contribution percentage by state
SELECT
    customer_state,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        100 * SUM(revenue) /
        (SELECT SUM(revenue) FROM ecommerce_sales),
        2
    ) AS revenue_percentage
FROM ecommerce_sales
GROUP BY customer_state
ORDER BY total_revenue DESC;


-- 5. Top 10 cities by revenue
SELECT
    customer_state,
    customer_city,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales
GROUP BY customer_state, customer_city
ORDER BY total_revenue DESC
LIMIT 10;
