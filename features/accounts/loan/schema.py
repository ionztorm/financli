CREATE_LOAN_CARDS_TABLE = """
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        balance REAL NOT NULL,
        monthly_charge REAL NOT NULL
    )
"""
