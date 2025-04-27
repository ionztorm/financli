CREATE_BANKS_TABLE = """
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        alias TEXT,
        balance REAL NOT NULL,
        limiter REAL NOT NULL
    )
"""
