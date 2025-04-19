class BankError(Exception):
    """Base exception for bank-related operations."""


class BankAccountNotFoundError(BankError):
    pass


class BankAccountHasBalanceError(BankError):
    pass


class BankAccountDeletionError(BankError):
    pass


class BankAccountValidationError(BankError):
    pass


class BankAccountWithdrawalError(BankError):
    pass
