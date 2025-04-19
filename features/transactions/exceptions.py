class TransactionError(Exception):
    """Base exception for transaction-related operations."""


class TransactionNotFoundError(TransactionError):
    """Raised when a specific transaction record is not found."""


class TransactionValidationError(TransactionError):
    """Raised when transaction data fails validation."""


class TransactionLoggingError(TransactionError):
    """Raised when a transaction fails to be logged (e.g. DB error)."""
