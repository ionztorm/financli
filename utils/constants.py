from utils.types import TableName

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
}
