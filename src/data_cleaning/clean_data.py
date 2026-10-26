import pandas as pd


class DataCleaner:

    def __init__(self, datasets):
        self.datasets = datasets

    def clean_all(self):

        cleaned_datasets = {}

        for name, df in self.datasets.items():

            df = self.basic_cleaning(df)

            cleaned_datasets[name] = df

        return cleaned_datasets


    def basic_cleaning(self, df):

        # Remove duplicate rows
        df = df.drop_duplicates()

        #reset index
        df = df.reset_index(drop=True)

        # Remove leading and trailing spaces from column names
        df.columns = df.columns.str.strip()

        # Remove leading and trailing spaces from text values
        text_columns = df.select_dtypes(include="object").columns

        for col in text_columns:
            df[col] = df[col].str.strip()

        # Convert date columns to datetime
        for col in df.columns:
            if "date" in col.lower() or "timestamp" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Fill missing product categories
        if "product_category_name" in df.columns:
            df["product_category_name"] = (
                df["product_category_name"]
                .fillna("Unknown")
            )

        return df
