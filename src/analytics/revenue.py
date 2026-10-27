import pandas as pd
import streamlit as st
from src.database.db_connection import engine

@st.cache_data(ttl=600)
def get_total_revenue():
    query = "SELECT ROUND(SUM(payment_value), 2) AS total_revenue FROM order_payments;"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def get_average_order_value():
    query = """
    SELECT ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS avg_order_value
    FROM order_payments;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def get_monthly_revenue():
    query = """
    SELECT o.order_purchase_timestamp, p.payment_value
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    WHERE o.order_purchase_timestamp IS NOT NULL
    """
    df = pd.read_sql(query, engine)
    df["month"] = pd.to_datetime(df["order_purchase_timestamp"]).dt.strftime("%Y-%m")
    trend = df.groupby("month", as_index=False)["payment_value"].sum()
    trend.rename(columns={"payment_value": "revenue"}, inplace=True)
    trend["revenue"] = trend["revenue"].round(2)
    return trend.sort_values("month").reset_index(drop=True)

@st.cache_data(ttl=600)
def get_top_categories():
    query = """
    SELECT pr.product_category_name AS category, ROUND(SUM(oi.price), 2) AS revenue
    FROM order_items oi
    JOIN products pr ON oi.product_id = pr.product_id
    WHERE pr.product_category_name IS NOT NULL
    GROUP BY pr.product_category_name
    ORDER BY revenue DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def get_top_sellers():
    query = """
    SELECT seller_id, ROUND(SUM(price), 2) AS revenue
    FROM order_items
    GROUP BY seller_id
    ORDER BY revenue DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)