import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from utils.constants import CURRENCY_SYMBOL
from features.accounts.base import Accounts
from features.accounts.exceptions import AccountHasBalanceError
from features.accounts.bank.exceptions import (
    BankAccountOpenError,
    BankAccountCloseError,
    BankAccountDepositError,
    BankAccountWithdrawalError,
)


class Bank(Accounts):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)

    @override
    def open(self, data: dict) -> None:
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(
                BankAccountOpenError, "Unable to open bank account."
            )
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(
                BankAccountCloseError, "Unable to close bank account."
            )
            raise wrapper(e) from e

    @override
    def withdraw(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance = float(account.get("balance", 0.0))
            limit = float(account.get("limiter", 0.0))

            if balance + limit < amount:
                raise AccountHasBalanceError(
                    "Withdrawal would go below the overdraft limit. "
                    f"Only {CURRENCY_SYMBOL}{balance + limit:.2f} "
                    "can be withdrawn"
                )

            super().withdraw(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                BankAccountWithdrawalError, "Unable to complete withdrawal."
            )
            raise wrapper(e) from e

    @override
    def deposit(self, id: int, amount: float) -> None:
        try:
            super().deposit(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                BankAccountDepositError, "Unable to complete deposit."
            )
            raise wrapper(e) from e
