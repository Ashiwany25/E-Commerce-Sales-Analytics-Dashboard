
-- PRODUCT CATEGORY SALES ANALYSIS

USE ecommerce_analytics;

-- 1. Top 10 categories by revenue
SELECT
    COALESCE(product_category_name, 'Unknown')
        AS category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS items_sold
FROM ecommerce_sales
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;


-- 2. Top 10 categories by number of items sold
SELECT
    COALESCE(product_category_name, 'Unknown')
        AS category,
    COUNT(*) AS items_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY category
ORDER BY items_sold DESC
LIMIT 10;


-- 3. Revenue contribution of top 10 categories
SELECT
    COALESCE(product_category_name, 'Unknown')
        AS category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        100 * SUM(revenue) /
        (SELECT SUM(revenue) FROM ecommerce_sales),
        2
    ) AS revenue_percentage
FROM ecommerce_sales
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Average selling price by category
SELECT
    COALESCE(product_category_name, 'Unknown')
        AS category,
    ROUND(AVG(price), 2) AS average_price,
    COUNT(*) AS items_sold
FROM ecommerce_sales
GROUP BY category
HAVING COUNT(*) >= 100
ORDER BY average_price DESC
LIMIT 10;
