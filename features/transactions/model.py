import sqlite3

from core.base import Table
from core.utils.types import (
    TableName,
)
from core.exceptions.db import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from core.utils.helpers import wrap_error
from features.transactions.service import TransactionService
from features.transactions.exceptions import TransactionLoggingError


class Transactions(Table):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.TRANSACTIONS)
        self._service = TransactionService(connection)

    def log(self, data: dict[str, str]) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrap_error(TransactionLoggingError, "Invalid transaction data")(e)
        except QueryExecutionError as e:
            wrap_error(TransactionLoggingError, "Failed to log transaction")(e)

    def amend(self, id: int, new_data: dict[str, str]) -> None:
        try:
            original = self.get_one(id)[0]
            self._service.reverse_effect(original)
            self._service.apply_effect(new_data)
            self._update(id, new_data)
        except RecordNotFoundError as e:
            wrap_error(TransactionLoggingError, f"Transaction {id} not found")(
                e
            )
        except QueryExecutionError as e:
            wrap_error(
                TransactionLoggingError, f"Failed to amend transaction {id}"
            )(e)

    def delete(self, id: int) -> None:
        try:
            transaction = self.get_one(id)[0]
            self._service.reverse_effect(transaction)
            self._delete(id)
        except QueryExecutionError as e:
            wrap_error(
                TransactionLoggingError, f"Failed to delete transaction {id}"
            )(e)
        except RecordNotFoundError as e:
            wrap_error(TransactionLoggingError, f"Transaction {id} not found")(
                e
            )
