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
