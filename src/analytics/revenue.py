import pandas as pd
import streamlit as st
from src.database.db_connection import engine

@st.cache_data
def get_total_revenue():
    query = "SELECT ROUND(SUM(payment_value), 2) AS Total_Revenue FROM order_payments;"
    return pd.read_sql(query, engine)

@st.cache_data
def get_total_orders():
    query = "SELECT COUNT(DISTINCT order_id) AS Total_Orders FROM orders;"
    return pd.read_sql(query, engine)

@st.cache_data
def get_average_order_value():
    query = """
    SELECT ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS Average_Order_Value
    FROM order_payments;
    """
    return pd.read_sql(query, engine)

# Alias in case app.py imports get_aov
get_aov = get_average_order_value

@st.cache_data
def get_monthly_revenue():
    query = """
    SELECT o.order_purchase_timestamp, p.payment_value
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    """
    df = pd.read_sql(query, engine)
    df['Month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.strftime('%Y-%m')
    trend = df.groupby('Month', as_index=False)['payment_value'].sum()
    trend.rename(columns={'payment_value': 'Monthly_Revenue'}, inplace=True)
    trend['Monthly_Revenue'] = trend['Monthly_Revenue'].round(2)
    return trend.sort_values('Month')

# Aliases for monthly revenue trend
get_monthly_revenue_trend = get_monthly_revenue

@st.cache_data
def get_top_categories():
    query = """
    SELECT pr.product_category_name, ROUND(SUM(oi.price), 2) AS Total_Revenue
    FROM order_items oi
    JOIN products pr ON oi.product_id = pr.product_id
    GROUP BY pr.product_category_name
    ORDER BY Total_Revenue DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    df['Total_Sales'] = df['Total_Revenue']
    return df

# Alias for product categories
get_top_product_categories = get_top_categories

@st.cache_data
def get_top_sellers():
    query = """
    SELECT seller_id, ROUND(SUM(price), 2) AS Total_Revenue
    FROM order_items
    GROUP BY seller_id
    ORDER BY Total_Revenue DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    df['Total_Sales'] = df['Total_Revenue']
    return df

@st.cache_data
def get_payment_distribution():
    query = """
    SELECT payment_type, COUNT(*) AS Total_Orders, ROUND(SUM(payment_value), 2) AS Total_Revenue
    FROM order_payments
    GROUP BY payment_type
    ORDER BY Total_Revenue DESC;
    """
    return pd.read_sql(query, engine)

# Aliases for payment methods
get_payment_method_distribution = get_payment_distribution
get_payment_methods = get_payment_distribution