import sqlite3
import unittest

from core.exceptions import RecordNotFoundError
from features.payable.bill.model import Bills
from features.payable.bill.schema import CREATE_BILLS_TABLE
from features.payable.bill.exceptions import (
    BillUpdateError,
    BillProviderCloseError,
    BillProviderCreationError,
)


class TestBills(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_BILLS_TABLE)
        self.connection.commit()
        self.bills = Bills(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS bills")
        self.connection.commit()
        self.connection.close()

    def test_open_bill_provider_valid(self) -> None:
        data = {
            "provider": "Electric Co",
            "monthly_charge": "75.50",
        }
        self.bills.open(data)
        result = self.bills.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "Electric Co",
                    "monthly_charge": 75.50,
                }
            ],
        )

    def test_open_bill_provider_missing_required(self) -> None:
        data = {
            "monthly_charge": "75.50",
        }
        with self.assertRaises(BillProviderCreationError) as context:
            self.bills.open(data)
        self.assertIn("Unable to create provider", str(context.exception))
        self.assertIn("Missing required fields", str(context.exception))

    def test_close_existing_provider(self) -> None:
        self.cursor.execute(
            "INSERT INTO bills (provider, monthly_charge) VALUES (?, ?)",
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
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )

    def test_update_bill_provider_valid(self) -> None:
        self.cursor.execute(
            "INSERT INTO bills (provider, monthly_charge) VALUES (?, ?)",
            ("Electric Co", 75.50),
        )
        self.connection.commit()

        update_data = {"provider": "Gas Co", "monthly_charge": "65.00"}
        self.bills.update(1, update_data)

        result = self.bills.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "Gas Co",
                    "monthly_charge": 65.00,
                }
            ],
        )

    def test_update_bill_provider_not_found(self) -> None:
        update_data = {"provider": "Water Co"}
        with self.assertRaises(BillUpdateError) as context:
            self.bills.update(999, update_data)
        self.assertIn("Unable to update bill details", str(context.exception))
        self.assertIn(
            "Record with ID 999 does not exist", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
