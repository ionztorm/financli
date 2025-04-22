class StoreCardError(Exception):
    """Base exception for credit card-related operations."""


class StoreCardAccountOpenError(StoreCardError):
    pass


class StoreCardAccountCloseError(StoreCardError):
    pass


class StoreCardAccountDepositError(StoreCardError):
    pass


class StoreCardAccountWithdrawalError(StoreCardError):
    pass
