import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from features.payable.base import Payable
from features.payable.subscription.exceptions import (
    SubscriptionCreationError,
    SubscriptionTerminationError,
)


class Subscriptions(Payable):
    def __init__(
        self, connection: sqlite3.Connection, table_name: TableName
    ) -> None:
        super().__init__(connection, table_name)

    @override
    def open(self, data: dict) -> None:
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(
                SubscriptionCreationError, "Unable to create subscription"
            )
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(
                SubscriptionTerminationError, "Unable to remove subscription"
            )
            raise wrapper(e) from e
