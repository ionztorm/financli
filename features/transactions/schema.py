CREATE_TRANSACTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        source_provider TEXT,
        source_type TEXT,
        source_id INTEGER,
        destination_provider TEXT,
        destination_type TEXT,
        destination_id INTEGER,
        description TEXT NOT NULL,
        amount REAL NOT NULL
    )
"""
