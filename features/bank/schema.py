CREATE_BANKS_TABLE = """
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        alias TEXT,
        balance REAL NOT NULL,
        overdraft REAL NOT NULL,
        is_source BOOLEAN NOT NULL DEFAULT 1,
        is_destination BOOLEAN NOT NULL DEFAULT 1
    )
"""
