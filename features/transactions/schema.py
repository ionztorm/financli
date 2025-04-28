CREATE_TRANSACTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        source_provider TEXT NOT NULL,
        source_type TEXT NOT NULL,
        source_id INTEGER NOT NULL,
        destination_provider TEXT,
        destination_type TEXT,
        destination_id INTEGER,
        description TEXT NOT NULL,
        amount REAL NOT NULL
    )
"""
