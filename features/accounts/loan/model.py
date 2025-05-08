import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from utils.constants import CURRENCY_SYMBOL
from features.accounts.base import Accounts
from features.accounts.exceptions import AccountHasBalanceError
from features.accounts.loan.exceptions import (
    LoanAccountOpenError,
    LoanAccountCloseError,
    LoanAccountUpdateError,
    LoanAccountDepositError,
)


class Loan(Accounts):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.LOANS)

    @override
    def open(self, data: dict) -> None:
        balance = data.get("balance") or 0.0
        data["balance"] = -balance
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(
                LoanAccountOpenError, "Unable to open loan account."
            )
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(
                LoanAccountCloseError, "Unable to close loan account."
            )
            raise wrapper(e) from e

    @override
    def withdraw(self, id: int, amount: float) -> None:
        raise NotImplementedError("You cannot withdraw from a loan account")

    @override
    def deposit(self, id: int, amount: float) -> None:
        try:
            account = self.get_one(id)[0]
            balance = float(account.get("balance", 0.0))
            new_balance = balance + amount
            if new_balance > 0:
                raise AccountHasBalanceError(
                    "Deposit would overpay the loan. "
                    f"Only {CURRENCY_SYMBOL}{balance} is due"
                )
            super().deposit(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                LoanAccountDepositError, "Unable to complete deposit."
            )
            raise wrapper(e) from e

    @override
    def update(self, id: int, data: dict) -> None:
        try:
            super().update(id, data)
        except Exception as e:
            wrapper = wrap_error(
                LoanAccountUpdateError, "Unable to update loan account "
            )
            raise wrapper(e) from e
