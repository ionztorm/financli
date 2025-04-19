CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    source_type TEXT NOT NULL,
    source_id INTEGER NOT NULL,

    destination_type TEXT,
    destination_id INTEGER,

    type TEXT NOT NULL,
    amount TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    vendor TEXT,
    item TEXT,
    category TEXT,
    notes TEXT,

    balance_after TEXT,
    status TEXT DEFAULT 'completed'
);
"""
