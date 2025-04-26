import sqlite3

from utils.helpers import wrap_error
from core.utility_service import UtilityService
from features.payable.base import PayOnly


class TransactionError(Exception):
    pass


class Controller:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.utility = UtilityService(db_connection)

    def list(self, data: dict) -> list[dict]:
        account_type = self.utility._get_account_type(data)
        model = self.utility._get_model(account_type)

        if "id" in data:
            id_ = self.utility._get_id(data)
            return model.get_one(id_)
        return model.get_many()

    def open(self, data: dict) -> None:
        account_type = self.utility._get_account_type(data)
        model = self.utility._get_model(account_type)
        model.open(data)

    def close(self, account_type: str, id: int) -> None:
        account_type = self.utility._require_non_empty_str(
            account_type, "Account type"
        )

        if not isinstance(id, int):
            raise ValueError(
                "Account ID must be an integer and cannot be empty."
            )

        model = self.utility._get_model(account_type)
        model.close(id)

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

    def transaction(self, data: dict) -> None:
        try:
            self.withdraw(
                {
                    "id": data.get("source_id"),
                    "account_type": data.get("source_account_type"),
                    "amount": data.get("amount"),
                }
            )

            if data.get("destination_account_type"):
                self.deposit(
                    {
                        "id": data.get("destination_id"),
                        "account_type": data.get("destination_account_type"),
                        "amount": data.get("amount"),
                    }
                )

            self._log_transaction(data)
        except Exception as e:
            raise wrap_error(TransactionError, "Transaction failed")(e) from e

    def _log_transaction(self, data: dict) -> None:
        pass  # TODO: Implement transaction logging
