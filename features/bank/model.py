import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from core.base_model import Table
from core.exceptions import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from features.bank.exceptions import (
    BankAccountDeletionError,
    BankAccountNotFoundError,
    BankAccountHasBalanceError,
    BankAccountValidationError,
    BankAccountWithdrawalError,
)


class Bank(Table):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)

    def open(self, data: dict[str, str]) -> None:
        try:
            self._create(data)
        except ValidationError as e:
            wrapper = wrap_error(
                BankAccountValidationError, "Could not open account"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                BankAccountValidationError, "Account creation failed"
            )
            raise wrapper(e) from e

    def close(self, id: int) -> None:
        try:
            self.get_one(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                BankAccountNotFoundError, "Cannot close account"
            )
            raise wrapper(e) from e

        try:
            self._delete(id)
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                BankAccountNotFoundError, "Account missing during deletion"
            )
            raise wrapper(e) from e
        except QueryExecutionError as e:
            wrapper = wrap_error(
                BankAccountDeletionError, "Could not delete account"
            )
            raise wrapper(e) from e

    def withdraw(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            overdraft_str = account.get("overdraft")

            balance = float(balance_str) if balance_str is not None else 0.0
            overdraft = (
                float(overdraft_str) if overdraft_str is not None else 0.0
            )
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                BankAccountNotFoundError, "Cannot perform transaction"
            )
            raise wrapper(e) from e

        if balance + overdraft < amount:
            raise BankAccountHasBalanceError(
                "Insufficient funds for this transaction."
            )

        new_balance = str(balance - amount)

        try:
            self._update(id, {"balance": new_balance})
        except QueryExecutionError as e:
            wrapper = wrap_error(
                BankAccountWithdrawalError,
                "Failed to update balance or log transaction",
            )
            raise wrapper(e) from e

    def deposit(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            balance = float(balance_str) if balance_str is not None else 0.0
        except RecordNotFoundError as e:
            wrapper = wrap_error(
                BankAccountNotFoundError, "Cannot perform transaction"
            )
            raise wrapper(e) from e

        new_balance = str(balance + amount)

        try:
            self._update(id, {"balance": new_balance})
        except QueryExecutionError as e:
            wrapper = wrap_error(
                BankAccountWithdrawalError,
                "Failed to update balance or log transaction",
            )
            raise wrapper(e) from e
