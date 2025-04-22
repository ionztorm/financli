import sqlite3

from typing import override

from utils.types import TableName
from utils.helpers import wrap_error
from features.accounts.base import Accounts
from features.accounts.credit_card.exceptions import (
    CreditCardAccountOpenError,
    CreditCardAccountCloseError,
    CreditCardAccountDepositError,
    CreditCardAccountWithdrawalError,
)


class CreditCard(Accounts):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, TableName.BANKS)

    @override
    def open(self, data: dict) -> None:
        try:
            super().open(data)
        except Exception as e:
            wrapper = wrap_error(
                CreditCardAccountOpenError,
                "Unable to open credit card account.",
            )
            raise wrapper(e) from e

    @override
    def close(self, id: int) -> None:
        try:
            super().close(id)
        except Exception as e:
            wrapper = wrap_error(
                CreditCardAccountCloseError,
                "Unable to close credit card account.",
            )
            raise wrapper(e) from e

    @override
    def withdraw(self, id: int, amount: float) -> None:
        try:
            super().withdraw(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                CreditCardAccountWithdrawalError,
                "Unable to complete withdrawal.",
            )
            raise wrapper(e) from e

    @override
    def deposit(self, id: int, amount: float) -> None:
        try:
            super().deposit(id, amount)
        except Exception as e:
            wrapper = wrap_error(
                CreditCardAccountDepositError, "Unable to complete deposit."
            )
            raise wrapper(e) from e
