class PayableError(Exception):
    """Base exception for account related operations."""


class PayableNotFoundError(PayableError):
    pass


class PayableDeletionError(PayableError):
    pass


class PayableOpenError(PayableError):
    pass


class PayablePaymentError(PayableError):
    pass
