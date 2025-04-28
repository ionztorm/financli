from enum import Enum


class TableName(Enum):
    BANKS = "banks"
    CREDITCARDS = "credit_cards"
    STORECARDS = "store_cards"
    LOANS = "loans"
    BILLS = "bills"
    SUBSCRIPTIONS = "subscriptions"
    TRANSACTIONS = "transactions"


class TransactionType(Enum):
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"
    PAY_ONLY = "pay_only"
    TRANSFER = "transfer"


class IDKeys(Enum):
    ID = "id"
    SOURCE_ID = "source_id"
    DESTINATION_ID = "destination_id"


class AccountTypeKeys(Enum):
    DEFAULT = "account_type"
    SOURCE_TYPE = "source_type"
    DESTINATION_TYPE = "destination_type"


class AccountRole(Enum):
    DEFAULT = "default"
    SOURCE = "source"
    DESTINATION = "destination"
