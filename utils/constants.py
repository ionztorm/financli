from utils.types import TableName
from utils.helpers import load_or_create_settings

CURRENCY_SYMBOL = currency = load_or_create_settings().get(
    "currency_symbol", "£"
)


TYPE_CONFIG = {
    TableName.BANKS: {
        "is_source": True,
        "is_destination": True,
        "display_name": "bank",
    },
    TableName.CREDITCARDS: {
        "is_source": True,
        "is_destination": True,
        "display_name": "credit card",
    },
    TableName.STORECARDS: {
        "is_source": True,
        "is_destination": True,
        "display_name": "store card",
    },
    TableName.LOANS: {
        "is_source": False,
        "is_destination": True,
        "display_name": "loan",
    },
    TableName.BILLS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "bill",
    },
    TableName.SUBSCRIPTIONS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "subscription",
    },
    TableName.TRANSACTIONS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "transaction",
    },
}

FIELD_MAP = {
    "bank": [
        ("provider", str),
        ("balance", float),
        ("alias", str),
        ("limiter", float),
    ],
    "credit card": [("provider", str), ("balance", float), ("limiter", float)],
    "store card": [("provider", str), ("balance", float), ("limiter", float)],
    "loan": [("provider", str), ("balance", float), ("monthly_charge", float)],
    "subscription": [("provider", str), ("monthly_charge", float)],
    "bill": [("provider", str), ("monthly_charge", float)],
}

TRANSACTION_TYPES = ["withdraw", "deposit", "pay another account", "payment"]
ACCOUNT_TYPES = list(FIELD_MAP.keys())
