
-- MONTHLY SALES GROWTH

USE ecommerce_analytics;

-- 1. Calculate month-over-month revenue growth

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(
            order_purchase_timestamp,
            '%Y-%m'
        ) AS sales_month,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM ecommerce_sales
    GROUP BY sales_month
),

revenue_comparison AS (
    SELECT
        sales_month,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)

SELECT
    sales_month,
    total_revenue,
    previous_month_revenue,

    ROUND(
        total_revenue - previous_month_revenue,
        2
    ) AS revenue_change,

    ROUND(
        100.0 *
        (total_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS growth_percentage

FROM revenue_comparison
ORDER BY sales_month;


-- 2. Identify the top 5 highest revenue months

SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS sales_month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales
GROUP BY sales_month
ORDER BY total_revenue DESC
LIMIT 5;
