CREATE_STORE_CARDS_TABLE = """
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        balance REAL NOT NULL,
        credit_limit REAL NOT NULL,
        is_source BOOLEAN NOT NULL DEFAULT 1,
        is_destination BOOLEAN NOT NULL DEFAULT 1
    )
"""
