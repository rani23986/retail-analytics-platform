# src/database/db_connection.py
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.database.seed_db import ensure_tables_exist

load_dotenv()

USER = os.getenv("DB_USER")
RAW_PASSWORD = os.getenv("DB_PASSWORD") or ""
PASSWORD = quote_plus(RAW_PASSWORD)
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT") or "3306"
DB = os.getenv("DB_NAME")

def get_engine():
    # Attempt MySQL connection if credentials are provided
    if USER and HOST and DB:
        try:
            database_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
            eng = create_engine(database_url, pool_pre_ping=True, connect_args={"connect_timeout": 10})
            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
            ensure_tables_exist(eng)
            return eng
        except Exception as e:
            print(f"MySQL connection or seeding warning ({e}). Falling back to built-in SQLite engine.")

    # Fallback to zero-config local SQLite database
    sqlite_url = "sqlite:///retail_analytics.db"
    eng = create_engine(sqlite_url)
    ensure_tables_exist(eng)
    return eng

engine = get_engine()