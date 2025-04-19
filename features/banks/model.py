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
from features.transactions.model import Transactions
from features.transactions.types import SourceAccountType, TransactionType


class Bank(Table):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)
        self._transactions = Transactions(connection)

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
            self._transactions.log(
                {
                    "source_type": SourceAccountType.BANK.value,
                    "source_id": str(id),
                    "type": TransactionType.WITHDRAWAL.value,
                    "amount": str(amount),
                    "status": "completed",
                }
            )
        except QueryExecutionError as e:
            wrap_error(
                BankAccountWithdrawalError,
                "Failed to update balance or log transaction",
            )(e)

    def deposit(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            balance = float(balance_str) if balance_str is not None else 0.0
        except RecordNotFoundError as e:
            wrap_error(BankAccountNotFoundError, "Cannot perform transaction")(
                e
            )

        new_balance = str(balance + amount)

        try:
            self._update(id, {"balance": new_balance})
            self._transactions.log(
                {
                    "source_type": SourceAccountType.BANK.value,
                    "source_id": str(id),
                    "type": TransactionType.DEPOSIT.value,
                    "amount": str(amount),
                    "status": "completed",
                }
            )
        except QueryExecutionError as e:
            wrap_error(
                BankAccountWithdrawalError,
                "Failed to update balance or log transaction",
            )(e)

    def spend(self, id: int, data: dict[str, str]) -> None:
        try:
            amount = float(data["amount"])
            account = self.get_one(id)[0]
            balance = float(account.get("balance") or 0.0)
            overdraft = float(account.get("overdraft") or 0.0)
        except (KeyError, ValueError) as e:
            wrap_error(BankAccountValidationError, "Missing or invalid amount")(
                e
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

        destination_type = data.get("destination_type")
        destination_id = data.get("destination_id")

        try:
            if destination_id and destination_type:
                self._transactions._service.apply_effect(
                    {
                        "source_type": SourceAccountType.BANK.value,
                        "source_id": str(id),
                        "destination_type": str(destination_type),
                        "destination_id": str(destination_id),
                        "type": TransactionType.SPEND.value,
                        "amount": str(amount),
                    }
                )
            else:
                new_balance = str(balance - amount)
                self._update(id, {"balance": new_balance})

            log_data: dict[str, str] = {
                "source_type": SourceAccountType.BANK.value,
                "source_id": str(id),
                "type": TransactionType.SPEND.value,
                "amount": str(amount),
                "status": "completed",
            }

            optional_fields = [
                "destination_type",
                "destination_id",
                "vendor",
                "item",
                "category",
                "notes",
            ]
            for field in optional_fields:
                value = data.get(field)
                if value is not None:
                    log_data[field] = str(value)

            self._transactions.log(log_data)

        except QueryExecutionError as e:
            wrap_error(
                BankAccountWithdrawalError,
                "Failed to complete spend transaction",
            )(e)
