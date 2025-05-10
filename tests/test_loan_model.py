import sqlite3
import unittest

from utils.loader import get_currency
from core.exceptions import RecordNotFoundError
from features.accounts.loan.model import Loan
from features.accounts.loan.schema import CREATE_LOAN_TABLE
from features.accounts.loan.exceptions import (
    LoanAccountOpenError,
    LoanAccountCloseError,
    LoanAccountUpdateError,
    LoanAccountDepositError,
)


class TestLoan(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_LOAN_TABLE)
        self.connection.commit()
        self.loan = Loan(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS loans")
        self.connection.commit()
        self.connection.close()

    def test_open_account_valid(self) -> None:
        data = {
            "provider": "LenderA",
            "balance": 5000.0,
            "monthly_charge": 250.0,
        }
        self.loan.open(data)
        result = self.loan.get_one(1)
        self.assertEqual(result[0]["provider"], "LenderA")
        self.assertEqual(result[0]["balance"], -5000.0)  # negated
        self.assertEqual(result[0]["monthly_charge"], 250.0)

    def test_open_account_validation_error(self) -> None:
        data = {"provider": "LenderA"}
        with self.assertRaises(LoanAccountOpenError) as context:
            self.loan.open(data)
        self.assertIn("Unable to open loan account", str(context.exception))
        self.assertIn("Missing required fields", str(context.exception))

    def test_deposit_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO loans (provider, balance, monthly_charge) "
            "VALUES (?, ?, ?)",
            ("LenderA", -5000.0, 250.0),
        )
        self.connection.commit()
        self.loan.deposit(1, 1000.0)
        result = self.loan.get_one(1)
        self.assertEqual(result[0]["balance"], -4000.0)

    def test_deposit_account_not_found(self) -> None:
        with self.assertRaises(LoanAccountDepositError) as context:
            self.loan.deposit(999, 100.0)
        self.assertIn("Unable to complete deposit", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )

    def test_deposit_overpayment(self) -> None:
        self.cursor.execute(
            "INSERT INTO loans (provider, balance, monthly_charge) "
            "VALUES (?, ?, ?)",
            ("LenderA", -100.0, 250.0),
        )
        self.connection.commit()
        with self.assertRaises(LoanAccountDepositError) as context:
            self.loan.deposit(1, 200.0)
        self.assertIn("Deposit would overpay the loan", str(context.exception))
        self.assertIn(
            f"Only {get_currency()}-100.0 is due",
            str(context.exception),
        )

    def test_withdraw_not_allowed(self) -> None:
        with self.assertRaises(NotImplementedError) as context:
            self.loan.withdraw(1, 100.0)
        self.assertEqual(
            str(context.exception), "You cannot withdraw from a loan account"
        )

    def test_update_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO loans (provider, balance, monthly_charge) "
            "VALUES (?, ?, ?)",
            ("LenderA", -500.0, 250.0),
        )
        self.connection.commit()
        self.loan.update(
            1, {"provider": "Updated Lender", "monthly_charge": "300.0"}
        )
        result = self.loan.get_one(1)
        self.assertEqual(result[0]["provider"], "Updated Lender")
        self.assertEqual(result[0]["monthly_charge"], 300.0)

    def test_update_account_not_found(self) -> None:
        with self.assertRaises(LoanAccountUpdateError) as context:
            self.loan.update(999, {"provider": "Test"})
        self.assertIn("Unable to update loan account", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )

    def test_close_account_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO loans (provider, balance, monthly_charge) "
            "VALUES (?, ?, ?)",
            ("LenderA", -300.0, 250.0),
        )
        self.connection.commit()
        self.loan.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.loan.get_one(1)

    def test_close_account_not_found(self) -> None:
        with self.assertRaises(LoanAccountCloseError) as context:
            self.loan.close(999)
        self.assertIn("Unable to close loan account", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
