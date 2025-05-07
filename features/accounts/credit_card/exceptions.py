class CreditCardError(Exception):
    """Base exception for credit card-related operations."""


class CreditCardAccountOpenError(CreditCardError):
    pass


class CreditCardAccountCloseError(CreditCardError):
    pass


class CreditCardAccountDepositError(CreditCardError):
    pass


class CreditCardAccountWithdrawalError(CreditCardError):
    pass


class CreditCardAccountUpdateError(CreditCardError):
    pass
