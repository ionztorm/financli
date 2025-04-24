import sqlite3
import unittest

from utils.types import TableName
from core.exceptions import RecordNotFoundError
from features.payable.bill.model import Bills
from features.payable.bill.schema import CREATE_BILLS_TABLE
from features.payable.bill.exceptions import (
    BillProviderCloseError,
    BillProviderCreationError,
)


class TestBills(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_BILLS_TABLE)
        self.connection.commit()
        self.bills = Bills(self.connection, TableName.BILLS)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS bills")
        self.connection.commit()
        self.connection.close()

    def test_open_bill_provider_valid(self) -> None:
        data = {
            "provider": "Electric Co",
            "monthly_bill": "75.50",
        }
        self.bills.open(data)
        result = self.bills.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "Electric Co",
                    "monthly_bill": 75.50,
                }
            ],
        )

    def test_open_bill_provider_missing_required(self) -> None:
        data = {
            "monthly_bill": "75.50",
        }
        with self.assertRaises(BillProviderCreationError) as context:
            self.bills.open(data)
        self.assertIn("Unable to create provider", str(context.exception))
        self.assertIn("Missing required fields", str(context.exception))

    def test_close_existing_provider(self) -> None:
        self.cursor.execute(
            "INSERT INTO bills (provider, monthly_bill) VALUES (?, ?)",
            ("Electric Co", 75.50),
        )
        self.connection.commit()
        self.bills.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.bills.get_one(1)

    def test_close_missing_provider(self) -> None:
        with self.assertRaises(BillProviderCloseError) as context:
            self.bills.close(999)
        self.assertIn("Unable to remove provider", str(context.exception))
        self.assertIn("No record found with ID 999", str(context.exception))


if __name__ == "__main__":
    unittest.main()
