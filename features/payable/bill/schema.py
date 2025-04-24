CREATE_BILLS_TABLE = """
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY,
        provider TEXT NOT NULL,
        monthly_bill REAL NOT NULL
    )
"""
