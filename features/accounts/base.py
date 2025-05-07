import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from core.base_model import Table
from core.exceptions import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from features.accounts.exceptions import (
    AccountOpenError,
    AccountUpdateError,
    AccountDeletionError,
    AccountNotFoundError,
    AccountWithdrawalError,
)


class Accounts(Table):
    def __init__(
        self, connection: sqlite3.Connection, table_name: TableName
    ) -> None:
        super().__init__(connection, table_name)

    def open(self, data: dict[str, str]) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrapper = wrap_error(AccountOpenError, "Account creation failed")
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(AccountOpenError, "Account creation failed")
            raise wrapper(e) from e

    def close(self, id: int) -> None:
        try:
            self.get_one(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                AccountNotFoundError, "Could not find account to close"
            )
            raise wrapper(e) from e

        try:
            self._delete(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                AccountNotFoundError, "Could not find account to close"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                AccountDeletionError, "Could not close account"
            )
            raise wrapper(e) from e

    def withdraw(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance = float(account.get("balance", 0.0))
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                AccountNotFoundError, "Could not find account for withdrawal"
            )
            raise wrapper(e) from e

        new_balance = str(balance - amount)

        try:
            self._update(id, {"balance": new_balance})
        except QueryExecutionError as e:
            wrapper = wrap_error(
                AccountWithdrawalError,
                "Failed to update balance",
            )
            raise wrapper(e) from e

    def deposit(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            balance = float(balance_str) if balance_str is not None else 0.0
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                AccountNotFoundError, "Could not find account for deposit"
            )
            raise wrapper(e) from e

        new_balance = str(balance + amount)

        try:
            self._update(id, {"balance": new_balance})
        except QueryExecutionError as e:
            wrapper = wrap_error(
                AccountWithdrawalError,
                "Failed to update balance",
            )
            raise wrapper(e) from e

    def update(self, id: int, data: dict) -> None:
        try:
            self.get_one(id)[0]
            self._update(id, data)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                AccountNotFoundError, "Could not find account to update "
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                AccountUpdateError, "Could not update account "
            )
            raise wrapper(e) from e
