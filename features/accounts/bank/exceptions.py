class BankError(Exception):
    """Base exception for bank-related operations."""


class BankAccountOpenError(BankError):
    pass


class BankAccountCloseError(BankError):
    pass


class BankAccountDepositError(BankError):
    pass


class BankAccountWithdrawalError(BankError):
    pass


class BankAccountNotFoundError(BankError):
    pass


class BankAccountUpdateError(BankError):
    pass
