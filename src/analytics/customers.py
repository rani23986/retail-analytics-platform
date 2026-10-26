import pandas as pd
import streamlit as st

from src.database.db_connection import engine


@st.cache_data(ttl=600)
def get_repeat_customers():

    query = """
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
    HAVING COUNT(o.order_id) > 1
    ORDER BY total_orders DESC;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_unique_customers():

    query = """
    SELECT
        COUNT(DISTINCT customer_unique_id) AS unique_customers
    FROM customers;
    """

    return pd.read_sql(query, engine)


@st.cache_data(ttl=600)
def get_average_rating():

    query = """
    SELECT
        ROUND(AVG(review_score),2) AS avg_rating
    FROM order_reviews;
    """

    return pd.read_sql(query, engine)