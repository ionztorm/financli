import sqlite3
import unittest

from datetime import datetime

from core.controller import Controller, TransactionError
from core.exceptions import RecordNotFoundError
from utils.constants import CURRENCY_SYMBOL
from features.transactions.schema import CREATE_TRANSACTIONS_TABLE
from features.accounts.bank.schema import CREATE_BANKS_TABLE
from features.accounts.bank.exceptions import (
    BankAccountOpenError,
    BankAccountCloseError,
    BankAccountDepositError,
    BankAccountWithdrawalError,
)


class TestController(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_BANKS_TABLE)
        self.cursor.execute(CREATE_TRANSACTIONS_TABLE)
        self.connection.commit()
        self.controller = Controller(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS banks")
        self.connection.commit()
        self.connection.close()

    def test_open_valid_bank_account(self) -> None:
        data = {
            "account_type": "bank",
            "provider": "BankX",
            "alias": "Main",
            "balance": "200.0",
            "limiter": "100.0",
            "is_source": "1",
            "is_destination": "1",
            "destination_provider": "BankX",
        }
        self.controller.open(data)
        result = self.controller.utility.bank_model.get_one(1)
        self.assertEqual(result[0]["provider"], "BankX")
        self.assertEqual(result[0]["balance"], 200.0)

    def test_open_invalid_bank_account_missing_fields(self) -> None:
        data = {
            "account_type": "bank",
            "provider": "BankX",
            "balance": "200.0",
        }
        with self.assertRaises(BankAccountOpenError):
            self.controller.open(data)

    def test_open_unsupported_source_type(self) -> None:
        data = {
            "account_type": "mystery",
            "provider": "BankX",
            "balance": "200.0",
        }
        with self.assertRaises(ValueError) as context:
            self.controller.open(data)
        self.assertIn("No model found for account type", str(context.exception))

    def test_close_valid_account(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.close("bank", 1)

        with self.assertRaises(RecordNotFoundError):
            self.controller.utility.bank_model.get_one(1)

    def test_close_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountCloseError):
            self.controller.close("bank", 999)

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.transactions.deposit(
            {
                "destination_type": "bank",
                "destination_id": 1,
                "amount": 50.0,
                "date": str(datetime.now()),
                "description": "Deposit of 50.0",
            }
        )
        result = self.controller.utility.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 250.0)

    def test_deposit_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountDepositError):
            self.controller.transactions.deposit(
                {
                    "destination_type": "bank",
                    "destination_id": 999,
                    "amount": 50.0,
                    "date": str(datetime.now()),
                    "description": "Deposit of 50.0",
                }
            )

    def test_withdraw_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.transactions.withdraw(
            {
                "source_type": "bank",
                "source_id": 1,
                "amount": 150.0,
                "date": str(datetime.now()),
                "description": "Withdrawal of 150.0",
            }
        )
        result = self.controller.utility.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 50.0)

    def test_withdraw_insufficient_funds(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 50.0, 10.0),
        )
        self.connection.commit()
        with self.assertRaises(BankAccountWithdrawalError) as context:
            self.controller.transactions.withdraw(
                {
                    "source_type": "bank",
                    "source_id": 1,
                    "amount": 100.0,
                    "date": str(datetime.now()),
                    "description": "Attempt to withdraw more than available",
                }
            )
        self.assertIn("Unable to complete withdrawal", str(context.exception))
        self.assertIn(
            "Withdrawal would go below the overdraft limit. "
            f"Only {CURRENCY_SYMBOL}60.00 can be withdrawn",
            str(context.exception),
        )

    def test_withdraw_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountWithdrawalError):
            self.controller.transactions.withdraw(
                {
                    "source_type": "bank",
                    "source_id": 999,
                    "amount": 20.0,
                    "date": str(datetime.now()),
                    "description": "Withdrawal attempt",
                }
            )

    def test_transaction_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Source", 300.0, 0.0),
        )
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Destination", 100.0, 0.0),
        )
        self.connection.commit()

        self.controller.transaction(
            {
                "transaction_type": "transfer",
                "source_type": "bank",
                "source_id": 1,
                "source_provider": "BankX",
                "destination_type": "bank",
                "destination_id": 2,
                "destination_provider": "BankX",
                "amount": 50.0,
                "date": str(datetime.now()),
                "description": "Transfer of 50.0 from Source to Destination",
            }
        )

        source = self.controller.utility.bank_model.get_one(1)
        dest = self.controller.utility.bank_model.get_one(2)
        self.assertEqual(source[0]["balance"], 250.0)
        self.assertEqual(dest[0]["balance"], 150.0)

    def test_transaction_invalid_source_account(self) -> None:
        with self.assertRaises(TransactionError) as context:
            self.controller.transaction(
                {
                    "transaction_type": "transfer",
                    "source_type": "bank",
                    "source_id": 999,
                    "destination_type": "bank",
                    "destination_id": 1,
                    "amount": 20.0,
                    "date": str(datetime.now()),
                    "description": "Invalid source account",
                }
            )
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )

    def test_deposit_with_string_id_and_amount(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 100.0, 0.0),
        )
        self.connection.commit()

        self.controller.transactions.deposit(
            {
                "destination_type": "bank",
                "destination_id": "1",
                "amount": "50.0",
                "date": str(datetime.now()),
                "description": "Deposit of 50.0",
            }
        )
        result = self.controller.utility.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 150.0)

    def test_withdraw_with_string_id_and_amount(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 0.0),
        )
        self.connection.commit()

        self.controller.transactions.withdraw(
            {
                "source_type": "bank",
                "source_id": "1",
                "amount": "75.0",
                "date": str(datetime.now()),
                "description": "Withdrawal of 75.0",
            }
        )
        result = self.controller.utility.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 125.0)

    def test_validate_source_type_missing(self) -> None:
        with self.assertRaises(ValueError):
            self.controller.open(
                {
                    "provider": "BankX",
                    "balance": "100.0",
                }
            )

    def test_validate_id_invalid_string(self) -> None:
        with self.assertRaises(ValueError):
            self.controller.transactions.deposit(
                {
                    "destination_type": "bank",
                    "destination_id": "abc",
                    "amount": 50.0,
                    "date": str(datetime.now()),
                    "description": "Invalid ID",
                }
            )

    def test_validate_amount_invalid_type(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 0.0),
        )
        self.connection.commit()

        with self.assertRaises(ValueError):
            self.controller.transactions.deposit(
                {
                    "destination_type": "bank",
                    "destination_id": 1,
                    "amount": [123],
                    "date": str(datetime.now()),
                    "description": "Invalid amount type",
                }
            )

    def test_deposit_unsupported_source_type(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.controller.transactions.deposit(
                {
                    "destination_type": "store_card",
                    "destination_id": 1,
                    "amount": 50.0,
                    "date": str(datetime.now()),
                    "description": "Unsupported account type",
                }
            )
        self.assertIn(
            "Unsupported destination account type", str(context.exception)
        )

    def test_withdraw_unsupported_source_type(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.controller.transactions.withdraw(
                {
                    "source_type": "loan",
                    "source_id": 1,
                    "amount": 50.0,
                    "date": str(datetime.now()),
                    "description": "Unsupported source type",
                }
            )
        self.assertIn("Unsupported source account type", str(context.exception))

    def test_list_many_accounts(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 100.0, 0.0),
        )
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankY", "Spare", 200.0, 50.0),
        )
        self.connection.commit()

        result = self.controller.list({"source_type": "bank"})
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["provider"], "BankX")
        self.assertEqual(result[1]["provider"], "BankY")

    def test_list_one_account_by_id(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 100.0, 0.0),
        )
        self.connection.commit()

        result = self.controller.list({"source_type": "bank", "id": 1})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["provider"], "BankX")

    def test_list_invalid_source_type(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.controller.list({"source_type": "alien_card"})
        self.assertIn("No model found for account type", str(context.exception))

    def test_list_invalid_id_type(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.controller.list({"source_type": "bank", "id": "abc"})
        self.assertIn(
            "id must be convertible to an integer", str(context.exception)
        )
