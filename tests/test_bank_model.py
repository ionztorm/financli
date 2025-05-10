import sqlite3
import unittest

from utils.loader import get_currency
from core.exceptions import RecordNotFoundError
from features.accounts.bank.model import Bank
from features.accounts.bank.schema import CREATE_BANKS_TABLE
from features.accounts.bank.exceptions import (
    BankAccountOpenError,
    BankAccountCloseError,
    BankAccountUpdateError,
    BankAccountDepositError,
    BankAccountWithdrawalError,
)


class TestBank(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_BANKS_TABLE)
        self.connection.commit()
        self.bank = Bank(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS banks")
        self.connection.commit()
        self.connection.close()

    def test_open_account_valid(self) -> None:
        data = {
            "provider": "BankA",
            "alias": "Savings",
            "balance": "100.0",
            "limiter": "50.0",
        }
        self.bank.open(data)
        result = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": 100.0,
                    "limiter": 50.0,
                }
            ],
        )

    def test_open_account_validation_error(self) -> None:
        data = {"provider": "BankA", "balance": "100.0"}
        with self.assertRaises(BankAccountOpenError) as context:
            self.bank.open(data)
        self.assertIn("Unable to open bank account", str(context.exception))
        self.assertIn("Missing required fields", str(context.exception))

    def test_close_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 0.0, 50.0),
        )
        self.connection.commit()
        self.bank.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.bank.get_one(1)

    def test_close_account_with_balance(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 10.0, 50.0),
        )
        self.connection.commit()
        with self.assertRaises(BankAccountCloseError):
            self.bank.close(1)

    def test_close_account_not_found(self) -> None:
        with self.assertRaises(BankAccountCloseError) as context:
            self.bank.close(999)
        self.assertIn("Unable to close bank account", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exis", str(context.exception)
        )

    def test_withdraw_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0),
        )
        self.connection.commit()
        self.bank.withdraw(1, 120.0)
        result = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": -20.0,
                    "limiter": 50.0,
                }
            ],
        )

    def test_withdraw_account_not_found(self) -> None:
        with self.assertRaises(BankAccountWithdrawalError) as context:
            self.bank.withdraw(999, 50.0)
        self.assertIn("Unable to complete withdrawal", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exis", str(context.exception)
        )

    def test_withdraw_insufficient_funds(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0),
        )
        self.connection.commit()
        with self.assertRaises(BankAccountWithdrawalError) as context:
            self.bank.withdraw(1, 200.0)
        self.assertEqual(
            str(context.exception),
            "Unable to complete withdrawal: Withdrawal would go below the "
            f"overdraft limit. Only {get_currency()}150.00 can be withdrawn",
        )
        self.assertIn(
            "Withdrawal would go below the overdraft limit. "
            "Only £150.00 can be withdrawn",
            str(context.exception),
        )

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "Savings", 100.0, 50.0),
        )
        self.connection.commit()
        self.bank.deposit(1, 50.0)
        result = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "Savings",
                    "balance": 150.0,
                    "limiter": 50.0,
                }
            ],
        )

    def test_deposit_account_not_found(self) -> None:
        with self.assertRaises(BankAccountDepositError) as context:
            self.bank.deposit(999, 50.0)
        self.assertIn("Unable to complete deposit", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )

    def test_update_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, alias, balance, limiter) "
            "VALUES (?, ?, ?, ?)",
            ("BankA", "OldAlias", 100.0, 50.0),
        )
        self.connection.commit()

        update_data = {"alias": "NewAlias", "limiter": "75.0"}
        self.bank.update(1, update_data)

        result = self.bank.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "BankA",
                    "alias": "NewAlias",
                    "balance": 100.0,
                    "limiter": 75.0,
                }
            ],
        )

    def test_update_account_not_found(self) -> None:
        update_data = {"alias": "UpdatedAlias"}
        with self.assertRaises(BankAccountUpdateError) as context:
            self.bank.update(999, update_data)
        self.assertIn("Unable to update bank account", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
