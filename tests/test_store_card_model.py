import sqlite3
import unittest

from core.exceptions import RecordNotFoundError
from features.accounts.store_card.model import StoreCard
from features.accounts.store_card.schema import (
    CREATE_STORE_CARDS_TABLE,
)
from features.accounts.store_card.exceptions import (
    StoreCardAccountOpenError,
    StoreCardAccountCloseError,
    StoreCardAccountDepositError,
    StoreCardAccountWithdrawalError,
)


class TestStoreCard(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_STORE_CARDS_TABLE)
        self.connection.commit()
        self.card = StoreCard(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS banks")
        self.connection.commit()
        self.connection.close()

    def test_open_account_valid(self) -> None:
        self.card.open(
            {
                "provider": "Target",
                "balance": "0.0",
                "credit_limit": "300.0",
                "is_source": "1",
                "is_destination": "1",
            }
        )
        result = self.card.get_one(1)
        self.assertEqual(result[0]["provider"], "Target")

    def test_open_account_validation_error(self) -> None:
        with self.assertRaises(StoreCardAccountOpenError):
            self.card.open({"provider": "Target"})

    def test_close_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, balance, credit_limit) "
            "VALUES (?, ?, ?)",
            ("Target", 0.0, 300.0),
        )
        self.connection.commit()
        self.card.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.card.get_one(1)

    def test_close_account_not_found(self) -> None:
        with self.assertRaises(StoreCardAccountCloseError):
            self.card.close(999)

    def test_withdraw_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, balance, credit_limit, "
            "is_source, is_destination) VALUES (?, ?, ?, ?, ?)",
            ("Target", -50.0, 300.0, 1, 1),
        )
        self.connection.commit()
        self.card.withdraw(1, 50.0)
        result = self.card.get_one(1)
        self.assertEqual(result[0]["balance"], -100.0)

    def test_withdraw_account_not_found(self) -> None:
        with self.assertRaises(StoreCardAccountWithdrawalError):
            self.card.withdraw(999, 50.0)

    def test_withdraw_insufficient_funds(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, balance, credit_limit) "
            "VALUES (?, ?, ?)",
            ("Target", 0.0, 100.0),
        )
        self.connection.commit()
        with self.assertRaises(StoreCardAccountWithdrawalError):
            self.card.withdraw(1, 200.0)

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, balance, credit_limit, "
            "is_source, is_destination) VALUES (?, ?, ?, ?, ?)",
            ("Target", -100.0, 300.0, 1, 1),
        )
        self.connection.commit()
        self.card.deposit(1, 100.0)
        result = self.card.get_one(1)
        self.assertEqual(result[0]["balance"], 0.0)

    def test_deposit_account_not_found(self) -> None:
        with self.assertRaises(StoreCardAccountDepositError):
            self.card.deposit(999, 50.0)

    def test_deposit_exceeds_balance_limit(self) -> None:
        self.cursor.execute(
            "INSERT INTO banks (provider, balance, credit_limit) "
            "VALUES (?, ?, ?)",
            ("Target", -50.0, 300.0),
        )
        self.connection.commit()
        with self.assertRaises(StoreCardAccountDepositError):
            self.card.deposit(1, 100.0)


if __name__ == "__main__":
    unittest.main()
