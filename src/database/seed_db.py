import os
import pandas as pd
import numpy as np
from sqlalchemy import inspect

def ensure_tables_exist(engine):
    """Checks if required tables exist in the database. If not, seeds them automatically."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    
    required_tables = {'orders', 'order_payments', 'order_items', 'customers', 'products', 'sellers', 'order_reviews'}
    if required_tables.issubset(existing_tables):
        return

    print("Initializing and seeding retail analytics database tables...")

    np.random.seed(42)
    n_orders = 1500
    n_customers = 1420
    n_products = 250
    n_sellers = 75

    categories = [
        'health_beauty', 'watches_gifts', 'bed_bath_table', 'sports_leisure',
        'computers_accessories', 'furniture_decor', 'housewares', 'cool_stuff',
        'auto', 'garden_tools', 'toys', 'baby', 'perfumery', 'telephony', 'electronics'
    ]
    cat_weights = [0.14, 0.13, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02]
    payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card']
    states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'GO', 'ES']
    cities = ['sao paulo', 'rio de janeiro', 'belo horizonte', 'curitiba', 'porto alegre', 'salvador', 'brasilia']

    # 1. Customers
    customer_ids = [f"c_{i:05d}" for i in range(n_orders)]
    unique_cust_pool = [f"u_{i:05d}" for i in range(n_customers)]
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_unique_id': np.random.choice(unique_cust_pool, size=n_orders),
        'customer_zip_code_prefix': np.random.randint(10000, 99999, size=n_orders),
        'customer_city': np.random.choice(cities, size=n_orders, p=[0.35, 0.20, 0.12, 0.10, 0.08, 0.08, 0.07]),
        'customer_state': np.random.choice(states, size=n_orders, p=[0.42, 0.13, 0.11, 0.06, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04])
    })

    # 2. Orders (Spanning 20 months so iloc[:-2] in app.py shows 18 clean months)
    order_ids = [f"ord_{i:05d}" for i in range(n_orders)]
    purchase_dates = pd.date_range(start="2017-01-05", end="2018-08-25", periods=n_orders)
    delivery_days = np.random.normal(loc=12.1, scale=4.5, size=n_orders).clip(2, 35).astype(int)
    est_days = np.random.normal(loc=23.4, scale=5.0, size=n_orders).clip(10, 40).astype(int)

    delivered_dates = purchase_dates + pd.to_timedelta(delivery_days, unit='D')
    estimated_dates = purchase_dates + pd.to_timedelta(est_days, unit='D')

    orders_df = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': customer_ids,
        'order_status': np.random.choice(['delivered', 'shipped', 'canceled', 'processing'], size=n_orders, p=[0.96, 0.02, 0.01, 0.01]),
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
        'product_category_name': np.random.choice(categories, size=n_products, p=cat_weights)
    })

    # 4. Sellers
    seller_ids = [f"seller_{i:04x}{i*17:04x}" for i in range(1, n_sellers + 1)]
    sellers_df = pd.DataFrame({
        'seller_id': seller_ids,
        'seller_city': np.random.choice(cities, size=n_sellers),
        'seller_state': np.random.choice(states, size=n_sellers)
    })

    # 5. Order Items
    n_items = 1800
    item_order_ids = np.random.choice(order_ids, size=n_items)
    prices = np.round(np.random.uniform(450.0, 14500.0, size=n_items), 2)
    freight = np.round(np.random.uniform(25.0, 180.0, size=n_items), 2)

    order_items_df = pd.DataFrame({
        'order_id': item_order_ids,
        'order_item_id': np.ones(n_items, dtype=int),
        'product_id': np.random.choice(product_ids, size=n_items),
        'seller_id': np.random.choice(seller_ids, size=n_items),
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

    # 7. Order Reviews
    reviews_df = pd.DataFrame({
        'review_id': [f"rev_{i:05d}" for i in range(n_orders)],
        'order_id': order_ids,
        'review_score': np.random.choice([5, 4, 3, 2, 1], size=n_orders, p=[0.57, 0.19, 0.08, 0.04, 0.12])
    })

    customers_df.to_sql('customers', engine, if_exists='replace', index=False)
    orders_df.to_sql('orders', engine, if_exists='replace', index=False)
    products_df.to_sql('products', engine, if_exists='replace', index=False)
    sellers_df.to_sql('sellers', engine, if_exists='replace', index=False)
    order_items_df.to_sql('order_items', engine, if_exists='replace', index=False)
    order_totals.to_sql('order_payments', engine, if_exists='replace', index=False)
    reviews_df.to_sql('order_reviews', engine, if_exists='replace', index=False)

    print("Database seeded with all 7 tables!")