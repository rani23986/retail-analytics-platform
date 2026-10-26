import os
import pandas as pd


class DataLoader:

    def __init__(self, data_path):
        self.data_path = data_path

    def load_all_datasets(self):

        if not os.path.isdir(self.data_path):
            raise FileNotFoundError(
                f"Data directory '{self.data_path}' does not exist. "
                "Download the Olist dataset and place the CSV files there."
            )

        datasets = {}

        csv_files = [
            file for file in os.listdir(self.data_path)
            if file.endswith(".csv")
        ]

        if not csv_files:
            raise FileNotFoundError(
                f"No CSV files found in '{self.data_path}'. "
                "Did you download the Olist dataset?"
            )

        for file in csv_files:
            path = os.path.join(self.data_path, file)
            datasets[file] = pd.read_csv(path)
            print(f"  Loaded: {file} ({len(datasets[file]):,} rows)")

        return datasets