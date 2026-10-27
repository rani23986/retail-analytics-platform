# src/database/seed_db.py
import os
import pandas as pd
import numpy as np
from sqlalchemy import inspect, text

def ensure_tables_exist(engine):
    """Checks if required tables exist in the database. If not, seeds them automatically."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = {'orders', 'order_payments', 'order_items', 'customers', 'products', 'sellers'}
    if required_tables.issubset(set(existing_tables)):
        return  # All tables already exist!

    print("Database tables missing. Initializing and seeding retail database...")

    # Check if local processed CSVs exist first
    processed_dir = "data/processed"
    if os.path.exists(os.path.join(processed_dir, "orders_clean.csv")):
        from src.database.database_loader import load_All_data
        load_All_data()
        return

    # Otherwise, generate realistic Olist-schema data (fits easily under 2MB for FreeSQLDatabase or SQLite)
    np.random.seed(42)
    n_orders = 1200
    n_customers = 950
    n_products = 200
    n_sellers = 60

    categories = [
        'bed_bath_table', 'health_beauty', 'sports_leisure', 'furniture_decor',
        'computers_accessories', 'housewares', 'watches_gifts', 'telephony',
        'garden_tools', 'auto', 'toys', 'cool_stuff', 'perfumery', 'baby', 'electronics'
    ]
    payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card']
    states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'GO', 'ES']
    cities = ['sao paulo', 'rio de janeiro', 'belo horizonte', 'curitiba', 'porto alegre', 'salvador', 'brasilia']

    # 1. Customers
    customer_ids = [f"cust_{i:04d}" for i in range(n_orders)]
    unique_cust_pool = [f"uniq_cust_{i:04d}" for i in range(n_customers)]
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_unique_id': np.random.choice(unique_cust_pool, size=n_orders),
        'customer_zip_code_prefix': np.random.randint(10000, 99999, size=n_orders),
        'customer_city': np.random.choice(cities, size=n_orders, p=[0.35, 0.20, 0.12, 0.10, 0.08, 0.08, 0.07]),
        'customer_state': np.random.choice(states, size=n_orders, p=[0.42, 0.13, 0.11, 0.06, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04])
    })

    # 2. Orders
    order_ids = [f"ord_{i:04d}" for i in range(n_orders)]
    purchase_dates = pd.date_range(start="2024-01-01", end="2025-12-31", periods=n_orders)
    delivery_days = np.random.randint(2, 22, size=n_orders)
    est_days = np.random.randint(7, 18, size=n_orders)

    delivered_dates = purchase_dates + pd.to_timedelta(delivery_days, unit='D')
    estimated_dates = purchase_dates + pd.to_timedelta(est_days, unit='D')

    orders_df = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': customer_ids,
        'order_status': np.random.choice(['delivered', 'shipped', 'canceled'], size=n_orders, p=[0.94, 0.04, 0.02]),
        'order_purchase_timestamp': purchase_dates.strftime('%Y-%m-%d %H:%M:%S'),
        'order_approved_at': (purchase_dates + pd.to_timedelta(2, unit='h')).strftime('%Y-%m-%d %H:%M:%S'),
        'order_delivered_carrier_date': (purchase_dates + pd.to_timedelta(2, unit='D')).strftime('%Y-%m-%d %H:%M:%S'),
        'order_delivered_customer_date': delivered_dates.strftime('%Y-%m-%d %H:%M:%S'),
        'order_estimated_delivery_date': estimated_dates.strftime('%Y-%m-%d %H:%M:%S')
    })

    # 3. Products
    product_ids = [f"prod_{i:04d}" for i in range(n_products)]
    products_df = pd.DataFrame({
        'product_id': product_ids,
        'product_category_name': np.random.choice(categories, size=n_products),
        'product_name_lenght': np.random.randint(20, 60, size=n_products),
        'product_description_lenght': np.random.randint(100, 1500, size=n_products),
        'product_photos_qty': np.random.randint(1, 6, size=n_products),
        'product_weight_g': np.random.randint(100, 10000, size=n_products),
        'product_length_cm': np.random.randint(10, 80, size=n_products),
        'product_height_cm': np.random.randint(5, 50, size=n_products),
        'product_width_cm': np.random.randint(10, 60, size=n_products)
    })

    # 4. Sellers
    seller_ids = [f"sell_{i:03d}" for i in range(n_sellers)]
    sellers_df = pd.DataFrame({
        'seller_id': seller_ids,
        'seller_zip_code_prefix': np.random.randint(10000, 99999, size=n_sellers),
        'seller_city': np.random.choice(cities, size=n_sellers),
        'seller_state': np.random.choice(states, size=n_sellers)
    })

    # 5. Order Items
    n_items = 1450
    item_order_ids = np.random.choice(order_ids, size=n_items)
    prices = np.round(np.random.uniform(25.0, 450.0, size=n_items), 2)
    freight = np.round(np.random.uniform(8.0, 45.0, size=n_items), 2)

    order_items_df = pd.DataFrame({
        'order_id': item_order_ids,
        'order_item_id': np.ones(n_items, dtype=int),
        'product_id': np.random.choice(product_ids, size=n_items),
        'seller_id': np.random.choice(seller_ids, size=n_items),
        'shipping_limit_date': pd.date_range(start="2024-01-05", periods=n_items).strftime('%Y-%m-%d %H:%M:%S'),
        'price': prices,
        'freight_value': freight
    })

    # 6. Order Payments
    order_totals = order_items_df.groupby('order_id')[['price', 'freight_value']].sum().sum(axis=1).reset_index()
    order_totals.columns = ['order_id', 'payment_value']
    order_totals['payment_value'] = order_totals['payment_value'].round(2)
    order_totals['payment_sequential'] = 1
    order_totals['payment_type'] = np.random.choice(payment_types, size=len(order_totals), p=[0.74, 0.18, 0.05, 0.03])
    order_totals['payment_installments'] = np.random.randint(1, 10, size=len(order_totals))

    # Write all tables to database
    customers_df.to_sql('customers', engine, if_exists='replace', index=False)
    orders_df.to_sql('orders', engine, if_exists='replace', index=False)
    products_df.to_sql('products', engine, if_exists='replace', index=False)
    sellers_df.to_sql('sellers', engine, if_exists='replace', index=False)
    order_items_df.to_sql('order_items', engine, if_exists='replace', index=False)
    order_totals.to_sql('order_payments', engine, if_exists='replace', index=False)

    print("Database seeded successfully!")