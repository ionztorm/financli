import sqlite3
import unittest

from core.controller import Controller
from core.exceptions import RecordNotFoundError
from features.bank.schema import CREATE_BANKS_TABLE
from features.bank.exceptions import (
    BankAccountNotFoundError,
    BankAccountHasBalanceError,
    BankAccountValidationError,
)


class TestController(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_BANKS_TABLE)
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
            "overdraft": "100.0",
            "is_source": "1",
            "is_destination": "1",
        }
        self.controller.open(data)
        result = self.controller.bank_model.get_one(1)
        self.assertEqual(result[0]["provider"], "BankX")
        self.assertEqual(result[0]["balance"], 200.0)

    def test_open_invalid_bank_account_missing_fields(self) -> None:
        data = {
            "account_type": "bank",
            "provider": "BankX",
            "balance": "200.0",
        }
        with self.assertRaises(BankAccountValidationError):
            self.controller.open(data)

    def test_open_unsupported_account_type(self) -> None:
        data = {
            "account_type": "mystery",
            "provider": "BankX",
            "balance": "200.0",
        }
        with self.assertRaises(ValueError) as context:
            self.controller.open(data)
        self.assertIn("Unsupported account type", str(context.exception))

    def test_close_valid_account(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.close("bank", 1)

        with self.assertRaises(RecordNotFoundError):
            self.controller.bank_model.get_one(1)

    def test_close_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountNotFoundError):
            self.controller.close("bank", 999)

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.deposit(
            {"account_type": "bank", "id": 1, "amount": 50.0}
        )
        result = self.controller.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 250.0)

    def test_deposit_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountNotFoundError):
            self.controller.deposit(
                {"account_type": "bank", "id": 999, "amount": 50.0}
            )

    def test_withdraw_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 200.0, 100.0),
        )
        self.connection.commit()
        self.controller.withdraw(
            {"account_type": "bank", "id": 1, "amount": 150.0}
        )
        result = self.controller.bank_model.get_one(1)
        self.assertEqual(result[0]["balance"], 50.0)

    def test_withdraw_insufficient_funds(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankX", "Main", 50.0, 10.0),
        )
        self.connection.commit()
        with self.assertRaises(BankAccountHasBalanceError):
            self.controller.withdraw(
                {"account_type": "bank", "id": 1, "amount": 100.0}
            )

    def test_withdraw_nonexistent_account(self) -> None:
        with self.assertRaises(BankAccountNotFoundError):
            self.controller.withdraw(
                {"account_type": "bank", "id": 999, "amount": 20.0}
            )


if __name__ == "__main__":
    unittest.main()
