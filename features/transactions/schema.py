CREATE_TRANSACTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        from_provider TEXT NOT NULL,
        from_type TEXT NOT NULL,
        from_id INTEGER NOT NULL,
        to_provider TEXT,
        to_type TEXT,
        to_id INTEGER,
        description TEXT NOT NULL,
        amount REAL NOT NULL
    )
"""
