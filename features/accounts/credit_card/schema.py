CREATE_CREDIT_CARDS_TABLE = """
    CREATE TABLE IF NOT EXISTS credit_cards (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        balance REAL NOT NULL,
        limiter REAL NOT NULL
    )
"""
