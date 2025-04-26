import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from features.payable.base import PayOnly
from features.payable.bill.exceptions import (
    BillProviderCloseError,
    BillProviderCreationError,
)


class Bills(PayOnly):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BILLS)

    @override
    def open(self, data: dict) -> None:
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(BillProviderCreationError, "Unable to create provider")
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(BillProviderCloseError, "Unable to remove provider")
            raise wrapper(e) from e
