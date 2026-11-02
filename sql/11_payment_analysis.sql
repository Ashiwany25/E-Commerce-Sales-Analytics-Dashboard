
-- PAYMENT METHOD ANALYSIS

USE ecommerce_analytics;

-- Each order can contain multiple items and payments.
-- Get one row per delivered order first.

CREATE OR REPLACE VIEW delivered_order_ids AS
SELECT DISTINCT order_id
FROM ecommerce_sales;


-- 1. Payment method usage
SELECT
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS total_orders,
    COUNT(*) AS payment_records
FROM ecommerce_payments p
INNER JOIN delivered_order_ids d
    ON p.order_id = d.order_id
GROUP BY p.payment_type
ORDER BY total_orders DESC;


-- 2. Total payment value by method
SELECT
    p.payment_type,
    ROUND(SUM(p.payment_value), 2) AS total_payment_value,
    ROUND(AVG(p.payment_value), 2) AS avg_payment_value
FROM ecommerce_payments p
INNER JOIN delivered_order_ids d
    ON p.order_id = d.order_id
GROUP BY p.payment_type
ORDER BY total_payment_value DESC;


-- 3. Percentage of delivered orders using each method
SELECT
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS total_orders,
    ROUND(
        100.0 * COUNT(DISTINCT p.order_id) /
        (SELECT COUNT(*) FROM delivered_order_ids),
        2
    ) AS order_percentage
FROM ecommerce_payments p
INNER JOIN delivered_order_ids d
    ON p.order_id = d.order_id
GROUP BY p.payment_type
ORDER BY total_orders DESC;


-- 4. Installment analysis for credit card payments
SELECT
    p.payment_installments,
    COUNT(DISTINCT p.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_payment_value
FROM ecommerce_payments p
INNER JOIN delivered_order_ids d
    ON p.order_id = d.order_id
WHERE p.payment_type = 'credit_card'
GROUP BY p.payment_installments
ORDER BY p.payment_installments;
