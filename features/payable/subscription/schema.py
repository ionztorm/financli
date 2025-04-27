CREATE_SUBSCRIPTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        monthly_charge REAL NOT NULL
    )
"""
