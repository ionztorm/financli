class TransactionError(Exception):
    pass


class TransactionLogError(TransactionError):
    pass


class TransactionNotFoundError(TransactionError):
    pass


class TransactionUpdateError(TransactionError):
    pass


class TransactionFieldsError(TransactionError):
    pass
