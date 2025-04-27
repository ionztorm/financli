import sqlite3
import unittest

from core.exceptions import RecordNotFoundError
from features.payable.subscription.model import Subscriptions
from features.payable.subscription.schema import CREATE_SUBSCRIPTIONS_TABLE
from features.payable.subscription.exceptions import (
    SubscriptionCreationError,
    SubscriptionTerminationError,
)


class TestSubscriptions(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute(CREATE_SUBSCRIPTIONS_TABLE)
        self.connection.commit()
        self.subscriptions = Subscriptions(self.connection)

    def tearDown(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS subscriptions")
        self.connection.commit()
        self.connection.close()

    def test_open_subscription_valid(self) -> None:
        data = {
            "provider": "Netflix",
            "monthly_charge": "15.00",
        }
        self.subscriptions.open(data)
        result = self.subscriptions.get_one(1)
        self.assertEqual(
            result,
            [
                {
                    "id": 1,
                    "provider": "Netflix",
                    "monthly_charge": 15.0,
                }
            ],
        )

    def test_open_subscription_missing_required(self) -> None:
        data = {"provider": "Netflix"}
        with self.assertRaises(SubscriptionCreationError) as context:
            self.subscriptions.open(data)
        self.assertIn("Unable to create subscription", str(context.exception))
        self.assertIn("Missing required fields", str(context.exception))

    def test_close_existing_subscription(self) -> None:
        self.cursor.execute(
            "INSERT INTO subscriptions (provider, monthly_charge) "
            "VALUES (?, ?)",
            ("Netflix", 15.0),
        )
        self.connection.commit()
        self.subscriptions.close(1)
        with self.assertRaises(RecordNotFoundError):
            self.subscriptions.get_one(1)

    def test_close_missing_subscription(self) -> None:
        with self.assertRaises(SubscriptionTerminationError) as context:
            self.subscriptions.close(999)
        self.assertIn("Unable to remove subscription", str(context.exception))
        self.assertIn("No record found with ID 999", str(context.exception))


if __name__ == "__main__":
    unittest.main()
