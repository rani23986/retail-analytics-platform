import pandas as pd
import streamlit as st

from src.database.db_connection import engine


@st.cache_data(ttl=600)
def get_total_revenue():

    query = """
    SELECT
        ROUND(SUM(payment_value), 2) AS Total_Revenue
    FROM order_payments;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_top_categories():

    query = """
    SELECT
        p.product_category_name AS category,
        ROUND(SUM(oi.price), 2) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
    ORDER BY revenue DESC
    LIMIT 10;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_top_sellers():

    query = """
    SELECT
        s.seller_id,
        ROUND(SUM(oi.price), 2) AS revenue
    FROM order_items oi
    JOIN sellers s
        ON oi.seller_id = s.seller_id
    GROUP BY s.seller_id
    ORDER BY revenue DESC
    LIMIT 10;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_average_order_value():

    query = """
    SELECT
        ROUND(
            SUM(payment_value) /
            COUNT(DISTINCT order_id),
            2
        ) AS avg_order_value
    FROM order_payments;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_monthly_revenue():

    query = """
    SELECT
        DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
        ROUND(SUM(op.payment_value),2) AS revenue
    FROM orders o
    JOIN order_payments op
        ON o.order_id = op.order_id
    GROUP BY DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m')
    ORDER BY month;
    """

    return pd.read_sql(query, engine)