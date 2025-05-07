import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from core.base_model import Table
from core.exceptions import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from features.payable.exceptions import (
    PayableOpenError,
    PayableUpdateError,
    PayableDeletionError,
    PayableNotFoundError,
)


class PayOnly(Table):
    def __init__(
        self, connection: sqlite3.Connection, table_name: TableName
    ) -> None:
        super().__init__(connection, table_name)

    def open(self, data: dict) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrapper = wrap_error(
                PayableOpenError, "Could not create new payable"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(PayableOpenError, "Payable creation failed")
            raise wrapper(e) from e

    def close(self, id: int) -> None:
        try:
            self.get_one(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(PayableNotFoundError, "Cannot close payable")
            raise wrapper(e) from e

        try:
            self._delete(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                PayableNotFoundError, "Unable to find payable for deletion"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                PayableDeletionError, "Could not delete payable"
            )
            raise wrapper(e) from e

    def update(self, id: int, data: dict) -> None:
        try:
            self.get_one(id)[0]
            self._update(id, data)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                PayableNotFoundError, "Could not find record to update "
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(PayableUpdateError, "Could not update record ")
            raise wrapper(e) from e
