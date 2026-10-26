class DatabaseLoader:

    TABLE_MAPPING = {
        "olist_customers_dataset.csv": "customers",
        "olist_orders_dataset.csv": "orders",
        "olist_products_dataset.csv": "products",
        "olist_sellers_dataset.csv": "sellers",
        "olist_order_items_dataset.csv": "order_items",
        "olist_order_payments_dataset.csv": "order_payments",
        "olist_order_reviews_dataset.csv": "order_reviews"
    }

    LOAD_ORDER = [
        "olist_customers_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv"
    ]

    def __init__(self, engine):
        self.engine = engine

    def load_dataset(self, df, table_name, replace=False):
        """Load a single DataFrame into the database.

        Args:
            df: The DataFrame to load.
            table_name: Target SQL table name.
            replace: If True, drop and recreate the table before inserting.
                     If False (default), append rows — only safe on a fresh DB.
        """
        if_exists_mode = "replace" if replace else "append"

        df.to_sql(
            table_name,
            con=self.engine,
            if_exists=if_exists_mode,
            index=False
        )

        print(f"✅ {table_name} loaded (mode={if_exists_mode})")

    def load_all(self, datasets, replace=False):
        """Load all datasets into the database in FK-safe order.

        Args:
            datasets: Dict mapping CSV filename → DataFrame.
            replace: Pass True to drop/recreate tables (prevents duplicate rows
                     when re-running main.py). Defaults to False (append).
        """
        for file_name in self.LOAD_ORDER:

            dataframe = datasets[file_name]

            table_name = self.TABLE_MAPPING[file_name]

            self.load_dataset(dataframe, table_name, replace=replace)

        print("\n🎉 Database Loaded Successfully!")