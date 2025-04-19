import sqlite3

from pathlib import Path

from features.banks.schema import CREATE_BANKS_TABLE
from features.transactions.schema import CREATE_TRANSACTIONS_TABLE

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "budget.db"


def create_data_path() -> None:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Establish a connection to the main app database and initialize tables."""
    create_data_path()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(CREATE_BANKS_TABLE)
    cursor.execute(CREATE_TRANSACTIONS_TABLE)
    # TODO: Add remaining tables

    conn.commit()
    return conn
