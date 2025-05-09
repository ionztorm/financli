import sqlite3
import unittest

from core.exceptions import RecordNotFoundError
from features.accounts.credit_card.model import CreditCard
from features.accounts.credit_card.schema import CREATE_CREDIT_CARDS_TABLE
from features.accounts.credit_card.exceptions import (
    CreditCardAccountOpenError,
    CreditCardAccountCloseError,
    CreditCardAccountUpdateError,
    CreditCardAccountDepositError,
    CreditCardAccountWithdrawalError,
)


class TestCreditCard(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_CREDIT_CARDS_TABLE)
        self.connection.commit()
        self.card = CreditCard(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS credit_cards")
        self.connection.commit()
        self.connection.close()

    def test_open_account_valid(self) -> None:
        self.card.open(
            {
                "provider": "Visa",
                "balance": "0.0",
                "limiter": "1000.0",
            }
        )
        result = self.card.get_one(1)
        self.assertEqual(result[0]["provider"], "Visa")

    def test_open_account_validation_error(self) -> None:
        with self.assertRaises(CreditCardAccountOpenError):
            self.card.open({"provider": "Visa"})

    def test_close_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", 0.0, 500.0),
        )
        self.connection.commit()
        self.card.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.card.get_one(1)

    def test_close_account_not_found(self) -> None:
        with self.assertRaises(CreditCardAccountCloseError):
            self.card.close(999)

    def test_withdraw_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", -100.0, 500.0),
        )
        self.connection.commit()
        self.card.withdraw(1, 100.0)
        result = self.card.get_one(1)
        self.assertEqual(result[0]["balance"], -200.0)

    def test_withdraw_account_not_found(self) -> None:
        with self.assertRaises(CreditCardAccountWithdrawalError):
            self.card.withdraw(999, 100.0)

    def test_withdraw_insufficient_funds(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", 0.0, 100.0),
        )
        self.connection.commit()
        with self.assertRaises(CreditCardAccountWithdrawalError):
            self.card.withdraw(1, 200.0)

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", -100.0, 500.0),
        )
        self.connection.commit()
        self.card.deposit(1, 100.0)
        result = self.card.get_one(1)
        self.assertEqual(result[0]["balance"], 0.0)

    def test_deposit_account_not_found(self) -> None:
        with self.assertRaises(CreditCardAccountDepositError):
            self.card.deposit(999, 100.0)

    def test_deposit_exceeds_balance_limit(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", -50.0, 500.0),
        )
        self.connection.commit()
        with self.assertRaises(CreditCardAccountDepositError):
            self.card.deposit(1, 100.0)

    def test_update_credit_card_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO credit_cards (provider, balance, limiter) "
            "VALUES (?, ?, ?)",
            ("Visa", -100.0, -1000.0),
        )
        self.connection.commit()

        update_data = {"provider": "Mastercard", "limiter": "-1500.0"}
        self.card.update(1, update_data)

        result = self.card.get_one(1)
        self.assertEqual(result[0]["provider"], "Mastercard")
        self.assertEqual(result[0]["limiter"], -1500.0)
        self.assertEqual(result[0]["balance"], -100.0)  # unchanged

    def test_update_credit_card_account_not_found(self) -> None:
        update_data = {"provider": "Amex"}
        with self.assertRaises(CreditCardAccountUpdateError) as context:
            self.card.update(999, update_data)
        self.assertIn(
            "Unable to update credit card account", str(context.exception)
        )
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
