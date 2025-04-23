from utils.types import TableName

CURRENCY_SYMBOL = "£"


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
}
