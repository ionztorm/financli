class LoanError(Exception):
    """Base exception for bank-related operations."""


class LoanAccountOpenError(LoanError):
    pass


class LoanAccountCloseError(LoanError):
    pass


class LoanAccountDepositError(LoanError):
    pass


class LoanAccountWithdrawalError(LoanError):
    pass
