import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from core.base_model import Table
from core.exceptions import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from features.transactions.exceptions import (
    TransactionLogError,
    TransactionFieldsError,
    TransactionUpdateError,
    TransactionNotFoundError,
)


class Transaction(Table):
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        super().__init__(db_connection, TableName.TRANSACTIONS)

    def log(self, data: dict) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrapper = wrap_error(
                TransactionLogError, "Could not log transaction"
            )
            raise wrapper(e) from e

    def update(self, id: int, data: dict) -> None:
        try:
            self.get_one(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                TransactionNotFoundError, "Could not find transaction"
            )
            raise wrapper(e) from e

        try:
            self._update(id, data)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                TransactionNotFoundError, "Could not find transaction"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                TransactionUpdateError, "Could not update transaction"
            )
            raise wrapper(e) from e
        except ValidationError as e:
            wrapper = wrap_error(
                TransactionFieldsError, "Could not update transaction"
            )
            raise wrapper(e) from e

    def delete(self, id: int) -> None:
        try:
            self._delete(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                TransactionNotFoundError, "Could not find transaction to delete"
            )
            raise wrapper(e) from e
