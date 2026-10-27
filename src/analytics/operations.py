import pandas as pd
import streamlit as st
from src.database.db_connection import engine

@st.cache_data
def get_average_delivery_time():
    query = """
    SELECT order_purchase_timestamp, order_delivered_customer_date
    FROM orders
    WHERE order_delivered_customer_date IS NOT NULL
    """
    df = pd.read_sql(query, engine)
    diff = (pd.to_datetime(df['order_delivered_customer_date']) - pd.to_datetime(df['order_purchase_timestamp'])).dt.days
    avg_days = round(diff.mean(), 2) if len(diff) > 0 else 0.0
    return pd.DataFrame({'Avg_Delivery_Days': [avg_days]})

@st.cache_data
def get_Order_status_distribution():
    query = """
    SELECT order_status, COUNT(*) AS Total_Orders
    FROM orders
    GROUP BY order_status
    ORDER BY Total_Orders DESC;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_late_deliveries():
    query = """
    SELECT COUNT(*) AS Late_Deliveries
    FROM orders
    WHERE order_delivered_customer_date > order_estimated_delivery_date;
    """
    return pd.read_sql(query, engine)