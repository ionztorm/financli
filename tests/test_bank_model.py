import sqlite3
import unittest

from core.exceptions import RecordNotFoundError
from features.bank.model import Bank
from features.bank.schema import CREATE_BANKS_TABLE
from features.bank.exceptions import (
    BankAccountNotFoundError,
    BankAccountHasBalanceError,
    BankAccountValidationError,
)


class TestBank(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a temporary SQLite database and table for testing."""
        self.connection: sqlite3.Connection = sqlite3.connect("test.db")
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS banks")
        self.connection.commit()
        self.cursor.execute(CREATE_BANKS_TABLE)
        self.connection.commit()
        self.bank: Bank = Bank(self.connection)

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.cursor.execute("DROP TABLE banks")
        self.connection.commit()
        self.connection.close()

    def test_open_account_valid(self) -> None:
        """Test opening a valid bank account."""
        data: dict[str, str] = {
            "provider": "BankA",
            "alias": "Savings",
            "balance": "100.0",
            "overdraft": "50.0",
            "is_source": "1",
            "is_destination": "1",
        }
        self.bank.open(data)
        result: list[dict[str, str]] = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": 100.0,
                    "overdraft": 50.0,
                    "is_source": 1,
                    "is_destination": 1,
                }
            ],
        )

    def test_open_account_validation_error(self) -> None:
        """Test opening a bank account with missing required fields."""
        data: dict[str, str] = {"provider": "BankA", "balance": "100.0"}
        with self.assertRaises(BankAccountValidationError) as context:
            self.bank.open(data)
        self.assertTrue(
            "Could not open account" in context.exception.args[0]
            or "Account creation failed" in context.exception.args[0]
        )
        self.assertTrue("Missing required fields" in context.exception.args[0])

    def test_close_account_valid(self) -> None:
        """Test closing an existing bank account."""
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0),
        )
        self.connection.commit()
        self.bank.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.bank.get_one(1)

    def test_close_account_not_found(self) -> None:
        """Test closing a non-existent account."""
        with self.assertRaises(BankAccountNotFoundError) as context:
            self.bank.close(999)
        self.assertTrue("Cannot close account" in context.exception.args[0])
        self.assertTrue(
            "No record found with ID 999" in context.exception.args[0]
        )

    def test_withdraw_valid(self) -> None:
        """Test withdrawing from a bank account with sufficient funds."""
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft, "
            "is_source, is_destination) VALUES (?, ?, ?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0, 1, 1),
        )
        self.connection.commit()
        self.bank.withdraw(1, 120.0)
        result: list[dict[str, str]] = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": -20.0,
                    "overdraft": 50.0,
                    "is_source": 1,
                    "is_destination": 1,
                }
            ],
        )

    def test_withdraw_account_not_found(self) -> None:
        """Test withdrawing from a non-existent account."""
        with self.assertRaises(BankAccountNotFoundError) as context:
            self.bank.withdraw(999, 50.0)
        self.assertTrue(
            "Cannot perform transaction" in context.exception.args[0]
        )
        self.assertTrue(
            "No record found with ID 999" in context.exception.args[0]
        )

    def test_withdraw_insufficient_funds(self) -> None:
        """Test withdrawing more than available balance and overdraft."""
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0),
        )
        self.connection.commit()
        with self.assertRaises(BankAccountHasBalanceError) as context:
            self.bank.withdraw(1, 200.0)
        self.assertEqual(
            context.exception.args[0],
            "Insufficient funds for this transaction.",
        )

    def test_deposit_valid(self) -> None:
        """Test depositing money into a bank account."""
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, overdraft, "
            "is_source, is_destination) VALUES (?, ?, ?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0, 1, 1),
        )
        self.connection.commit()
        self.bank.deposit(1, 50.0)
        result: list[dict[str, str]] = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": 150.0,
                    "overdraft": 50.0,
                    "is_source": 1,
                    "is_destination": 1,
                }
            ],
        )

    def test_deposit_account_not_found(self) -> None:
        """Test depositing into a non-existent account."""
        with self.assertRaises(BankAccountNotFoundError) as context:
            self.bank.deposit(999, 50.0)
        self.assertTrue(
            "Cannot perform transaction" in context.exception.args[0]
        )
        self.assertTrue(
            "No record found with ID 999" in context.exception.args[0]
        )


if __name__ == "__main__":
    unittest.main()
