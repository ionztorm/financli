import sqlite3

from pathlib import Path

from features.payable.bill.schema import CREATE_BILLS_TABLE
from features.accounts.bank.schema import CREATE_BANKS_TABLE
from features.accounts.store_card.schema import CREATE_STORE_CARDS_TABLE
from features.accounts.credit_card.schema import CREATE_CREDIT_CARDS_TABLE
from features.payable.subscription.schema import CREATE_SUBSCRIPTIONS_TABLE

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "financli.db"


def create_data_path() -> None:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Establish a connection to the main app database and initialize tables."""
    create_data_path()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(CREATE_BANKS_TABLE)
    cursor.execute(CREATE_CREDIT_CARDS_TABLE)
    cursor.execute(CREATE_BILLS_TABLE)
    cursor.execute(CREATE_STORE_CARDS_TABLE)
    cursor.execute(CREATE_SUBSCRIPTIONS_TABLE)
    # TODO: Add remaining tables

    conn.commit()
    return conn
