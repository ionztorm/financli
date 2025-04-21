class AccountError(Exception):
    """Base exception for account related operations."""


class AccountNotFoundError(AccountError):
    pass


class AccountHasBalanceError(AccountError):
    pass


class AccountDeletionError(AccountError):
    pass


class AccountValidationError(AccountError):
    pass


class AccountWithdrawalError(AccountError):
    pass
