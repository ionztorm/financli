import logging
import sqlite3

from typing import Callable, Optional

from utils.types import TableName
from utils.constants import TYPE_CONFIG
from features.bank.model import Bank

logging.basicConfig(level=logging.ERROR)


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

    def _get_open_method(self, account_type: str) -> Optional[Callable]:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.open
        # TODO: Implement for credit card
        return None

    def open(self, data: dict) -> None:
        account_type = data.get("account_type")
        if not isinstance(account_type, str):
            raise ValueError(
                "Account type must be a string and cannot be empty."
            )

        open_method = self._get_open_method(account_type)
        if open_method:
            open_method(data)
        else:
            valid_types = self.source_types + self.destination_types
            raise ValueError(
                f"Unsupported account type: {account_type}. "
                f"Valid types: {', '.join(valid_types)}"
            )

    def _get_close_method(self, account_type: str) -> Optional[Callable]:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.close
        # TODO: Implement for credit card
        return None

    def close(self, account_type: str, id: int) -> None:
        if not isinstance(account_type, str):
            raise ValueError(
                "Account type must be a string and cannot be empty."
            )

        close_method = self._get_close_method(account_type)
        if close_method:
            close_method(id)
        else:
            valid_types = self.source_types + self.destination_types
            raise ValueError(
                f"Unsupported account type: {account_type}. "
                f"Valid types: {', '.join(valid_types)}"
            )

    def _get_deposit_method(self, account_type: str) -> Optional[Callable]:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.deposit
        # TODO: Implement for credit card
        return None

    def deposit(self, data: dict) -> None:
        account_type = data.get("account_type")
        if not isinstance(account_type, str):
            raise ValueError(
                "Account type must be a string and cannot be empty."
            )

        deposit_method = self._get_deposit_method(account_type)
        if deposit_method:
            deposit_method(data["id"], data["amount"])
        else:
            raise ValueError(
                f"Unsupported account type for deposit: {account_type}. "
                f"Valid types: {', '.join(self.destination_types)}"
            )

    def _get_withdraw_method(self, account_type: str) -> Optional[Callable]:
        if account_type == TYPE_CONFIG[TableName.BANKS]["display_name"]:
            return self.bank_model.withdraw
        # TODO: Implement for credit card
        return None

    def withdraw(self, data: dict) -> None:
        account_type = data.get("account_type")
        if not isinstance(account_type, str):
            raise ValueError(
                "Account type must be a string and cannot be empty."
            )

        withdraw_method = self._get_withdraw_method(account_type)
        if withdraw_method:
            withdraw_method(data["id"], data["amount"])
        else:
            raise ValueError(
                f"Unsupported account type for withdrawal: {account_type}. "
                f"Valid types: {', '.join(self.source_types)}"
            )
