from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    SPEND = "spend"
    PAYMENT = "payment"
    TRANSFER = "transfer"


class AccountType(str, Enum):
    BANK = "bank"
    CREDIT_CARD = "credit_card"
    STORE_CARD = "store_card"


class DestinationType(str, Enum):
    BANK = "bank"
    CREDIT_CARD = "credit_card"
    STORE_CARD = "store_card"
    BILL = "bill"
    SUBSCRIPTION = "subscription"


class TransactionCategory(str, Enum):
    GROCERIES = "groceries"
    UTILITIES = "utilities"
    RENT = "rent"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    HEALTHCARE = "healthcare"
    OTHER = "other"
