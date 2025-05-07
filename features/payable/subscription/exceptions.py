class SubscriptionError(Exception):
    """Base exception for credit card-related operations."""


class SubscriptionCreationError(SubscriptionError):
    pass


class SubscriptionTerminationError(SubscriptionError):
    pass


class SubscriptionUpdateError(SubscriptionError):
    pass
