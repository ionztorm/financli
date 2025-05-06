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
        "is_pay_only": False,
    },
    TableName.CREDITCARDS: {
        "is_source": True,
        "is_destination": True,
        "display_name": "credit card",
        "is_pay_only": False,
    },
    TableName.STORECARDS: {
        "is_source": True,
        "is_destination": True,
        "display_name": "store card",
        "is_pay_only": False,
    },
    TableName.LOANS: {
        "is_source": False,
        "is_destination": True,
        "display_name": "loan",
        "is_pay_only": False,
    },
    TableName.BILLS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "bill",
        "is_pay_only": True,
    },
    TableName.SUBSCRIPTIONS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "subscription",
        "is_pay_only": True,
    },
    TableName.TRANSACTIONS: {
        "is_source": False,
        "is_destination": False,
        "display_name": "transaction",
        "is_pay_only": False,
    },
}

TRANSACTION_TYPES = ["withdraw", "deposit", "pay another account", "payment"]
ACCOUNT_TYPES = ["bank", "credit card", "store card", "bill", "subscription"]
