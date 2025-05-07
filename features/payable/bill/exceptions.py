class BillError(Exception):
    """Base exception for credit card-related operations."""


class BillProviderCreationError(BillError):
    pass


class BillProviderCloseError(BillError):
    pass


class BillUpdateError(BillError):
    pass
