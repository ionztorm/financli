import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from utils.constants import CURRENCY_SYMBOL
from features.accounts.base import Accounts
from features.accounts.exceptions import AccountHasBalanceError
from features.accounts.store_card.exceptions import (
    StoreCardAccountOpenError,
    StoreCardAccountCloseError,
    StoreCardAccountUpdateError,
    StoreCardAccountDepositError,
    StoreCardAccountWithdrawalError,
)


class StoreCard(Accounts):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.STORECARDS)

    @override
    def open(self, data: dict) -> None:
        balance = data.get("balance")
        limiter = data.get("limiter")

        if balance is not None:
            data["balance"] = -float(balance)
        if limiter is not None:
            data["limiter"] = -float(limiter)

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
            account = self.get_one(id)[0]
            balance = float(account.get("balance", 0.0))
            if balance != 0.0:
                raise AccountHasBalanceError(
                    "This account has a balance of "
                    f"{CURRENCY_SYMBOL}{balance:.2f}. "
                    "Please recfity this with a transaction."
                )
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountCloseError,
                "Unable to close store card account. ",
            )
            raise wrapper(e) from e

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
                    "Withdrawal would go over the credit limit. "
                    f"Only {CURRENCY_SYMBOL}{limit - balance} can be withdrawn"
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
                    "Deposit would overpay the card. "
                    f"Only {CURRENCY_SYMBOL}{balance} is due"
                )

            super().deposit(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountDepositError, "Unable to complete deposit."
            )
            raise wrapper(e) from e

    @override
    def update(self, id: int, data: dict) -> None:
        try:
            super().update(id, data)
        except Exception as e:
            wrapper = wrap_error(
                StoreCardAccountUpdateError,
                "Unable to update credit card account ",
            )
            raise wrapper(e) from e
