from src.data_cleaning.load_data import DataLoader
from src.data_cleaning.clean_data import DataCleaner
from src.data_cleaning.save_data import DataSaver
from src.database.db_connection import engine
from src.database.database_loader import DatabaseLoader

DATA_PATH = "data/raw"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retail Analytics ETL Pipeline")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Drop and recreate DB tables before loading (prevents duplicate data).",
    )
    args = parser.parse_args()

    loader = DataLoader(DATA_PATH)
    datasets = loader.load_all_datasets()

    cleaner = DataCleaner(datasets)
    cleaned_datasets = cleaner.clean_all()

    print(f"Loaded {len(cleaned_datasets)} cleaned datasets.")

    saver = DataSaver("data/cleaned")
    saver.save_all(cleaned_datasets)

    db_loader = DatabaseLoader(engine)
    db_loader.load_all(cleaned_datasets, replace=args.reload)