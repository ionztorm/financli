CREATE_SUBSCRIPTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        subscription_charge REAL NOT NULL
    )
"""
