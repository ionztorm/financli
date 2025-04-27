import sqlite3

from core.utility_service import UtilityService
from features.payable.base import PayOnly


class TransactionService:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.utility = UtilityService(db_connection)

    def deposit(self, data: dict) -> None:
        account_type, account_id = self.utility._get_account_type_and_id(data)
        amount = self.utility._get_amount(data)

        model = self.utility._get_destination_model(account_type)
        if isinstance(model, PayOnly):
            raise ValueError(f"Cannot deposit into {account_type}.")
        model.deposit(account_id, amount)

    def withdraw(self, data: dict) -> None:
        account_type, account_id = self.utility._get_account_type_and_id(data)
        amount = self.utility._get_amount(data)

        model = self.utility._get_source_model(account_type)
        if isinstance(model, PayOnly):
            raise ValueError(f"Cannot withdraw from {account_type}.")
        model.withdraw(account_id, amount)

    def log_transaction(self) -> None:
        raise NotImplementedError
