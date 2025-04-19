import sqlite3

from core.base import Table
from core.constants import CURRENCY_SYMBOL
from core.utils.types import TableName
from core.exceptions.db import (
    ValidationError,
    QueryExecutionError,
    RecordNotFoundError,
)
from core.utils.helpers import wrap_error
from features.banks.exceptions import (
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
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            overdraft_str = account.get("overdraft")

            balance = float(balance_str) if balance_str is not None else 0.0
            overdraft = (
                float(overdraft_str) if overdraft_str is not None else 0.0
            )

        except RecordNotFoundError as e:
            wrap_error(BankAccountNotFoundError, "Cannot perform transaction")(
                e
            )

        if balance + overdraft < amount:
            raise BankAccountHasBalanceError(
                f"Insufficient funds for this transaction. "
                f"Total available: {CURRENCY_SYMBOL}{balance + overdraft} "
                f"(including overdraft of {CURRENCY_SYMBOL}{overdraft})."
            )

        new_balance = str(balance - amount)

        try:
            self._update(id, {"balance": new_balance})
        except QueryExecutionError as e:
            wrap_error(
                BankAccountWithdrawalError, "Failed to update account balance"
            )(e)

        # TODO: log transaction

    def deposit(self, id: int, amount: float) -> None:
        # TODO: Implement deposit logic
        pass

    def spend(self, id: int, data: dict[str, str]) -> None:
        # TODO: Implement spending logic
        pass
