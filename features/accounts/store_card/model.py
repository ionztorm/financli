import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from features.accounts.base import Accounts
from features.accounts.exceptions import AccountHasBalanceError
from features.accounts.store_card.exceptions import (
    StoreCardAccountOpenError,
    StoreCardAccountCloseError,
    StoreCardAccountDepositError,
    StoreCardAccountWithdrawalError,
)


class StoreCard(Accounts):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)

    @override
    def open(self, data: dict) -> None:
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountOpenError,
                "Unable to open store card account.",
            )
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountCloseError,
                "Unable to close store card account.",
            )
            raise wrapper(e) from e

    @override
    def withdraw(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance = float(account.get("balance", 0.0))
            limit = float(account.get("limiter", 0.0))

            if (balance - amount) < -limit:
                raise AccountHasBalanceError(
                    "Insufficient funds for this transaction."
                )

            super().withdraw(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountWithdrawalError,
                "Unable to complete withdrawal.",
            )
            raise wrapper(e) from e

    @override
    def deposit(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance_str = account.get("balance")
            balance = float(balance_str) if balance_str else 0.0

            new_balance = balance + amount
            if new_balance > 0:
                raise AccountHasBalanceError(
                    "Deposit would result in a positive balance on the "
                    "store card account."
                )

            super().deposit(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountDepositError, "Unable to complete deposit."
            )
            raise wrapper(e) from e
