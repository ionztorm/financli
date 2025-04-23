import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from utils.constants import TYPE_CONFIG
from utils.model_types import ModelType
from features.accounts.bank.model import Bank
from features.accounts.store_card.model import StoreCard
from features.accounts.credit_card.model import CreditCard


class TransactionError(Exception):
    pass


class Controller:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.bank_model = Bank(db_connection)
        self.credit_card_model = CreditCard(db_connection)
        self.store_card_model = StoreCard(db_connection)

        self.valid_account_types = self._get_valid_account_types()
        self.source_types = self.valid_account_types["source_types"]
        self.destination_types = self.valid_account_types["dest_types"]

        self._model_map: dict[str, ModelType] = {
            TYPE_CONFIG[TableName.BANKS]["display_name"]: self.bank_model,
            TYPE_CONFIG[TableName.CREDITCARDS][
                "display_name"
            ]: self.credit_card_model,
            TYPE_CONFIG[TableName.STORECARDS][
                "display_name"
            ]: self.store_card_model,
        }

    def _get_valid_account_types(self) -> dict:
        source_types = []
        dest_types = []
        for config in TYPE_CONFIG.values():
            if config.get("is_source"):
                source_types.append(config.get("display_name"))
            if config.get("is_destination"):
                dest_types.append(config.get("display_name"))
        return {
            "source_types": source_types,
            "dest_types": dest_types,
        }

    def _require_non_empty_str(self, value: object, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value

    def _get_model(self, account_type: str) -> ModelType:
        model = self._model_map.get(account_type)
        if not model:
            raise ValueError(f"No model found for account type: {account_type}")
        return model

    def _get_source_model(self, account_type: str) -> ModelType:
        if account_type not in self.source_types:
            raise ValueError(f"Unsupported source account type: {account_type}")
        return self._get_model(account_type)

    def _get_destination_model(self, account_type: str) -> ModelType:
        if account_type not in self.destination_types:
            raise ValueError(
                f"Unsupported destination account type: {account_type}"
            )
        return self._get_model(account_type)

    def list(self, data: dict) -> list[dict]:
        account_type = self._get_account_type(data)
        model = self._get_model(account_type)

        if "id" in data:
            id_ = self._get_id(data)
            return model.get_one(id_)
        return model.get_many()

    def open(self, data: dict) -> None:
        account_type = self._get_account_type(data)
        model = self._get_model(account_type)
        model.open(data)

    def close(self, account_type: str, id: int) -> None:
        account_type = self._require_non_empty_str(account_type, "Account type")

        if not isinstance(id, int):
            raise ValueError(
                "Account ID must be an integer and cannot be empty."
            )

        model = self._get_model(account_type)
        model.close(id)

    def deposit(self, data: dict) -> None:
        account_type, account_id = self._get_account_type_and_id(data)
        amount = self._get_amount(data)

        model = self._get_destination_model(account_type)
        model.deposit(account_id, amount)

    def withdraw(self, data: dict) -> None:
        account_type, account_id = self._get_account_type_and_id(data)
        amount = self._get_amount(data)

        model = self._get_source_model(account_type)
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

    def _get_account_type_and_id(self, data: dict) -> tuple[str, int]:
        account_type = self._get_account_type(data)
        account_id = self._get_id(data)
        return account_type, account_id

    def _get_amount(self, data: dict) -> float:
        amount_raw = data.get("amount")
        if amount_raw is None:
            raise ValueError("Amount is required.")
        try:
            return float(amount_raw)
        except (ValueError, TypeError) as e:
            raise ValueError("Amount must be convertible to a float.") from e

    def _get_id(self, data: dict) -> int:
        raw_id = data.get("id")
        if raw_id is None:
            raise ValueError("Account ID is required.")
        try:
            return int(raw_id)
        except (ValueError, TypeError) as e:
            raise ValueError(
                "Account ID must be convertible to an integer."
            ) from e

    def _get_account_type(self, data: dict) -> str:
        return self._require_non_empty_str(
            data.get("account_type"), "Account type"
        )
