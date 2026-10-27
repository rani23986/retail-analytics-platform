import pandas as pd
import streamlit as st
from src.database.db_connection import engine

@st.cache_data
def get_total_customers():
    query = "SELECT COUNT(DISTINCT customer_unique_id) AS Total_Customers FROM customers;"
    return pd.read_sql(query, engine)

@st.cache_data
def get_repeat_customers():
    query = """
    SELECT COUNT(*) AS Repeat_Customers
    FROM (
        SELECT c.customer_unique_id
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_unique_id
        HAVING COUNT(o.order_id) > 1
    ) AS repeat_table;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_top_customer_states():
    query = """
    SELECT customer_state, COUNT(DISTINCT customer_unique_id) AS Total_Customers
    FROM customers
    GROUP BY customer_state
    ORDER BY Total_Customers DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_top_customer_cities():
    query = """
    SELECT customer_city, COUNT(DISTINCT customer_unique_id) AS Total_Customers
    FROM customers
    GROUP BY customer_city
    ORDER BY Total_Customers DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

get_customer_states = get_top_customer_states
get_top_states = get_top_customer_states
get_customer_cities = get_top_customer_cities
get_top_cities = get_top_customer_cities