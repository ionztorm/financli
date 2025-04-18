import sqlite3

from models.base import Table
from utils.types import TableName
from utils.helpers import wrap_error
from utils.exceptions.db import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from utils.exceptions.bank import (
    BankAccountDeletionError,
    BankAccountNotFoundError,
    BankAccountHasBalanceError,
    BankAccountValidationError,
)


class Bank(Table):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)

    def open(self, data: dict[str, str]) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrap_error(BankAccountValidationError, "Could not open account")(e)
        except QueryExecutionError as e:
            wrap_error(BankAccountValidationError, "Account creation failed")(e)

    def close(self, id: int) -> None:
        try:
            account = self.get_one(id)
        except RecordNotFoundError as e:
            wrap_error(BankAccountNotFoundError, "Cannot close account")(e)

        balance_str = account[0].get("balance")
        if balance_str is not None and float(balance_str) > 0.0:
            raise BankAccountHasBalanceError(
                "Cannot close account: balance must be zero."
            )

        try:
            self._delete(id)
        except RecordNotFoundError as e:
            wrap_error(
                BankAccountNotFoundError, "Account missing during deletion"
            )(e)
        except QueryExecutionError as e:
            wrap_error(BankAccountDeletionError, "Could not delete account")(e)

    def withdraw(self, id: int, amount: float) -> None:
        # TODO: Implement withdrawal logic
        pass

    def deposit(self, id: int, amount: float) -> None:
        # TODO: Implement deposit logic
        pass

    def spend(self, id: int, amount: float) -> None:
        # TODO: Implement spending logic
        pass
