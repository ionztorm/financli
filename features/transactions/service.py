import sqlite3

from core.exceptions.db import QueryExecutionError
from core.utils.helpers import wrap_error
from features.banks.model import Bank
from features.transactions.types import SourceAccountType
from features.transactions.exceptions import TransactionLoggingError


class TransactionService:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.bank = Bank(connection)
        # TODO: Add more models: credit_card, bills, etc.

    def reverse_effect(self, transaction: dict[str, str]) -> None:
        try:
            amount = float(transaction["amount"])

            source_type = transaction["source_type"]
            source_id = int(transaction["source_id"])

            if source_type not in SourceAccountType._value2member_map_:
                raise TransactionLoggingError(
                    f"Invalid source_type: {source_type}"
                )

            if source_type == SourceAccountType.BANK.value:
                self.bank.deposit(source_id, amount)

            # TODO: account for other source types

            destination_type = transaction.get("destination_type")
            destination_id = transaction.get("destination_id")

            if destination_type:
                if destination_type not in SourceAccountType._value2member_map_:
                    raise TransactionLoggingError(
                        f"Invalid destination_type: {destination_type}"
                    )

                if (
                    destination_type == SourceAccountType.BANK.value
                    and destination_id
                ):
                    self.bank.withdraw(int(destination_id), amount)

                # TODO: account for other destination types

        except QueryExecutionError as error:
            wrap_error(
                TransactionLoggingError, "Failed to reverse transaction effect"
            )(error)

    def apply_effect(self, transaction: dict[str, str]) -> None:
        try:
            amount = float(transaction["amount"])

            source_type = transaction["source_type"]
            source_id = int(transaction["source_id"])

            if source_type not in SourceAccountType._value2member_map_:
                raise TransactionLoggingError(
                    f"Invalid source_type: {source_type}"
                )

            if source_type == SourceAccountType.BANK.value:
                self.bank.withdraw(source_id, amount)

            # TODO: handle other source types

            destination_type = transaction.get("destination_type")
            destination_id = transaction.get("destination_id")

            if destination_type:
                if destination_type not in SourceAccountType._value2member_map_:
                    raise TransactionLoggingError(
                        f"Invalid destination_type: {destination_type}"
                    )

                if (
                    destination_type == SourceAccountType.BANK.value
                    and destination_id
                ):
                    self.bank.deposit(int(destination_id), amount)

                # TODO: handle other destination types

        except QueryExecutionError as error:
            wrap_error(
                TransactionLoggingError, "Failed to apply transaction effect"
            )(error)
