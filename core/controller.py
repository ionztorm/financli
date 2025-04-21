import sqlite3

from typing import Callable

from utils.types import TableName
from utils.helpers import wrap_error
from utils.constants import TYPE_CONFIG
from features.bank.model import Bank


# TODO: Create transaction domain errors
class TransactionError(Exception):
    pass


class Controller:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.bank_model = Bank(db_connection)

        self.valid_account_types = self._get_valid_account_types()
        self.source_types = self.valid_account_types["source_types"]
        self.destination_types = self.valid_account_types["dest_types"]

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

    def _get_open_method(self, account_type: str) -> Callable | None:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.open
        # TODO: Implement for credit card
        # TODO: Implement for store card
        # TODO: Implement for subscriptions
        # TODO: Implement for bills
        # TODO: Implement for loans
        return None

    def open(self, data: dict) -> None:
        account_type = self._require_non_empty_str(
            data.get("account_type"), "Account type"
        )

        open_method = self._get_open_method(account_type)
        if open_method:
            open_method(data)
        else:
            valid_types = self.source_types + self.destination_types
            raise ValueError(
                f"Unsupported account type '{account_type}' for open. "
                f"Supported types: {', '.join(valid_types)}"
            )

    def _get_close_method(self, account_type: str) -> Callable | None:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.close
        # TODO: Implement for credit card
        # TODO: Implement for store card
        # TODO: Implement for subscriptions
        # TODO: Implement for bills
        # TODO: Implement for loans
        return None

    def close(self, account_type: str, id: int) -> None:
        account_type = self._require_non_empty_str(account_type, "Account type")

        if not isinstance(id, int):
            raise ValueError(
                "Account ID must be an integer and cannot be empty."
            )

        close_method = self._get_close_method(account_type)
        if close_method:
            close_method(id)
        else:
            valid_types = self.source_types + self.destination_types
            raise ValueError(
                f"Unsupported account type '{account_type}' for close. "
                f"Supported types: {', '.join(valid_types)}"
            )

    def _get_deposit_method(self, account_type: str) -> Callable | None:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.deposit
        # TODO: Implement for credit card
        # TODO: Implement for store card
        # TODO: Implement for subscriptions
        # TODO: Implement for bills
        # TODO: Implement for loans
        return None

    def deposit(self, data: dict) -> None:
        account_type, account_id = self._validate_account_type_and_id(data)
        amount = self._validate_amount(data)

        deposit_method = self._get_deposit_method(account_type)
        if deposit_method:
            deposit_method(account_id, amount)
        else:
            raise ValueError(
                f"Unsupported account type '{account_type}' for deposit. "
                "Supported destination types: "
                f"{', '.join(self.destination_types)}"
            )

    def _get_withdraw_method(self, account_type: str) -> Callable | None:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.withdraw
        # TODO: Implement for credit card
        # TODO: Implement for store card
        # TODO: Implement for subscriptions
        # TODO: Implement for bills
        # TODO: Implement for loans
        return None

    def withdraw(self, data: dict) -> None:
        account_type, account_id = self._validate_account_type_and_id(data)
        amount = self._validate_amount(data)

        withdraw_method = self._get_withdraw_method(account_type)
        if withdraw_method:
            withdraw_method(account_id, amount)
        else:
            raise ValueError(
                f"Unsupported account type '{account_type}' for withdrawal. "
                f"Supported source types: {', '.join(self.source_types)}"
            )

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
            wrap_error(TransactionError, "Transaction failed")(e)

    def _log_transaction(self, data: dict) -> None:
        pass  # TODO: Implement transaction logging

    def _validate_account_type_and_id(self, data: dict) -> tuple[str, int]:
        account_type = self._require_non_empty_str(
            data.get("account_type"), "Account type"
        )

        account_id_raw = data.get("id")
        if account_id_raw is None:
            raise ValueError("Account ID is required.")

        try:
            account_id = int(account_id_raw)
        except (ValueError, TypeError) as e:
            raise ValueError(
                "Account ID must be convertible to an integer."
            ) from e

        return account_type, account_id

    def _validate_amount(self, data: dict) -> float:
        amount_raw = data.get("amount")
        if amount_raw is None:
            raise ValueError("Amount is required.")

        try:
            return float(amount_raw)
        except (ValueError, TypeError) as e:
            raise ValueError("Amount must be convertible to a float.") from e
