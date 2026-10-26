import pandas as pd
import streamlit as st

from src.database.db_connection import engine


@st.cache_data(ttl=600)
def get_order_status_breakdown():
    """Returns the count and percentage of orders by status."""

    query = """
    SELECT
        order_status,
        COUNT(*) AS total_orders,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
    FROM orders
    GROUP BY order_status
    ORDER BY total_orders DESC;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_delivery_performance():
    """Returns average actual vs estimated delivery times (days) for delivered orders."""

    query = """
    SELECT
        ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 2)
            AS avg_actual_delivery_days,
        ROUND(AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)), 2)
            AS avg_estimated_delivery_days
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_late_deliveries():
    """Returns count and percentage of orders delivered after the estimated date."""

    query = """
    SELECT
        COUNT(*) AS total_delivered,
        SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END)
            AS late_deliveries,
        ROUND(
            SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END)
            * 100.0 / COUNT(*), 2
        ) AS late_pct
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL;
    """

    return pd.read_sql(query, engine)
