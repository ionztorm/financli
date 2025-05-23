import sqlite3

from utils.types import IDKeys, AccountTypeKeys, TransactionType
from utils.helpers import wrap_error
from core.utility_service import UtilityService
from core.transaction_service import TransactionService
from features.transactions.model import Transaction
from features.transactions.exceptions import TransactionError


class Controller:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.utility = UtilityService(db_connection)
        self.transactions = TransactionService(db_connection)

    def list(self, data: dict) -> list[dict]:
        account_type = self.utility._get_account_type(
            data, AccountTypeKeys.DEFAULT
        )
        model = self.utility._get_model(account_type)

        if "id" in data:
            id_ = self.utility._get_id(data, IDKeys.ID)
            return model.get_one(id_)
        return model.get_many()

    def open(self, data: dict) -> None:
        account_type = self.utility._get_account_type(
            data, AccountTypeKeys.DEFAULT
        )
        model = self.utility._get_model(account_type)
        if not isinstance(model, Transaction):
            model.open(data)

    def close(self, account_type: str, id: int) -> None:
        account_type = self.utility._require_non_empty_str(
            account_type, "Account type"
        )

        _id = self.utility._get_id({"id": id}, IDKeys.ID)

        if not isinstance(_id, int):
            raise ValueError(
                "Account ID must be an integer and cannot be empty."
            )

        model = self.utility._get_model(account_type)
        if not isinstance(model, Transaction):
            model.close(_id)

    def transaction(self, data: dict) -> None:
        try:
            transaction_type_str = self.utility._require_non_empty_str(
                data.get("transaction_type"), "transaction_type"
            )

            try:
                transaction_type = TransactionType[transaction_type_str.upper()]
            except KeyError as e:
                raise ValueError(
                    f"Invalid transaction type: {transaction_type_str}"
                ) from e

            match transaction_type:
                case TransactionType.WITHDRAW | TransactionType.PAY_ONLY:
                    self.transactions.withdraw(data)

                case TransactionType.DEPOSIT:
                    self.transactions.deposit(data)

                case TransactionType.TRANSFER:
                    self.transactions.withdraw(data)
                    self.transactions.deposit(data)

                case _:
                    raise ValueError(
                        f"Invalid transaction type: {transaction_type_str}"
                    )

            self.transactions.log_transaction(data)

        except Exception as e:
            raise wrap_error(TransactionError, "Transaction failed")(e) from e

    def update(self, data: dict) -> None:
        account_type = self.utility._get_account_type(
            data, AccountTypeKeys.DEFAULT
        )
        id = self.utility._get_id(data, IDKeys.ID)
        model = self.utility._get_model(account_type)
        if not isinstance(model, Transaction):
            model.update(id, data)
