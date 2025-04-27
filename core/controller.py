import sqlite3

from utils.helpers import wrap_error
from core.utility_service import UtilityService
from core.transaction_service import TransactionService


class TransactionError(Exception):
    pass


class Controller:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.utility = UtilityService(db_connection)
        self.transactions = TransactionService(db_connection)

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

        _id = self.utility._get_id({"id": id})

        if not isinstance(_id, int):
            raise ValueError(
                "Account ID must be an integer and cannot be empty."
            )

        model = self.utility._get_model(account_type)
        model.close(_id)

    def transaction(self, data: dict) -> None:
        try:
            self.transactions.withdraw(
                {
                    "id": data.get("source_id"),
                    "account_type": data.get("source_account_type"),
                    "amount": data.get("amount"),
                }
            )

            if data.get("destination_account_type"):
                self.transactions.deposit(
                    {
                        "id": data.get("destination_id"),
                        "account_type": data.get("destination_account_type"),
                        "amount": data.get("amount"),
                    }
                )

        except Exception as e:
            raise wrap_error(TransactionError, "Transaction failed")(e) from e
