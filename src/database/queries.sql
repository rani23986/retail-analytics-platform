-- =====================================================
-- Total Revenue
-- =====================================================

SELECT
    ROUND(SUM(payment_value),2) AS Total_Revenue
FROM order_payments;

-- =====================================================
-- Monthly Revenue Trend
-- =====================================================

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%%Y-%%m') AS month,
    ROUND(SUM(op.payment_value),2) AS revenue
FROM orders o
JOIN order_payments op
ON o.order_id = op.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m')
ORDER BY month;

-- =====================================================
-- Top 10 Product Categories by Revenue
-- =====================================================

SELECT
    p.product_category_name AS category,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 5;

-- =====================================================
-- Top 10 Sellers by Revenue
-- =====================================================

SELECT
    s.seller_id,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY s.seller_id
ORDER BY revenue DESC
LIMIT 10;

-- =====================================================
-- Repeat Customers
-- =====================================================

SELECT
    c.customer_unique_id,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
HAVING COUNT(o.order_id) > 1
ORDER BY total_orders DESC;

-- =====================================================
-- Average Order Value
-- =====================================================

SELECT
    ROUND(
        SUM(payment_value) /
        COUNT(DISTINCT order_id),
        2
    ) AS avg_order_value
FROM order_payments;

-- =====================================================
-- Unique Customers
-- =====================================================

SELECT
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;

-- =====================================================
-- Average Rating
-- =====================================================

SELECT
    ROUND(AVG(review_score),2) AS avg_rating
FROM order_reviews;

-- =====================================================
-- Delivery Performance (Estimated vs Actual)
-- =====================================================

SELECT
    ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 2) AS avg_actual_delivery_days,
    ROUND(AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)), 2) AS avg_estimated_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;

-- =====================================================
-- Order Status Breakdown
-- =====================================================

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;