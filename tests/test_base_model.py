import sqlite3
import unittest

from utils.types import TableName
from core.base_model import Table
from core.exceptions import (
    ValidationError,
    ColumnMismatchError,
    RecordNotFoundError,
)


class TestTable(unittest.TestCase):
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    table: Table

    def setUp(self) -> None:
        """Set up a temporary SQLite database and table for testing."""
        self.connection = sqlite3.connect(
            "test.db"
        )  # Creating a temporary database
        self.cursor = self.connection.cursor()

        # Drop the table if it already exists to avoid the "table already exists" error
        self.cursor.execute(
            "DROP TABLE IF EXISTS banks"
        )  # Adjusted table name based on TableName enum
        self.connection.commit()

        # Creating a sample table
        self.cursor.execute(
            """
            CREATE TABLE banks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
            """
        )
        self.connection.commit()

        # Initialize Table instance with the correct TableName enum member
        self.table = Table(self.connection, TableName.BANKS)

    def tearDown(self) -> None:
        """Clean up after each test."""
        # Drop the table and close the connection
        self.cursor.execute(
            "DROP TABLE banks"
        )  # Adjusted table name based on TableName enum
        self.connection.commit()
        self.connection.close()

    def test_get_one_existing(self) -> None:
        """Test fetching one record by ID."""
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("John Doe", 100.0),
        )
        self.connection.commit()

        result: list[dict[str, str]] = self.table.get_one(1)
        self.assertEqual(
            result, [{"id": 1, "name": "John Doe", "balance": 100.0}]
        )

    def test_get_one_not_found(self) -> None:
        """Test fetching one record when the ID doesn't exist."""
        with self.assertRaises(RecordNotFoundError):
            self.table.get_one(999)  # Non-existent ID

    def test_get_many(self) -> None:
        """Test fetching all records."""
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("John Doe", 100.0),
        )
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("Jane Smith", 200.0),
        )
        self.connection.commit()

        result: list[dict[str, str]] = self.table.get_many()
        self.assertEqual(len(result), 2)

    def test_create_valid(self) -> None:
        """Test inserting a valid record."""
        data: dict[str, str] = {"name": "John Doe", "balance": "100.0"}
        self.table._create(data)

        result: list[dict[str, str]] = self.table.get_one(1)
        self.assertEqual(
            result, [{"id": 1, "name": "John Doe", "balance": 100.0}]
        )

    def test_create_invalid_missing_field(self) -> None:
        """Test inserting an invalid record (missing required field)."""
        data: dict[str, str] = {"name": "John Doe"}
        with self.assertRaises(ValidationError):
            self.table._create(data)  # Missing 'balance'

    def test_update_valid(self) -> None:
        """Test updating an existing record."""
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("John Doe", 100.0),
        )
        self.connection.commit()

        data: dict[str, str] = {"name": "John Updated", "balance": "150.0"}
        self.table._update(1, data)

        result: list[dict[str, str]] = self.table.get_one(1)
        self.assertEqual(
            result, [{"id": 1, "name": "John Updated", "balance": 150.0}]
        )

    def test_update_not_found(self) -> None:
        """Test updating a non-existent record."""
        data: dict[str, str] = {"name": "John Doe", "balance": "100.0"}
        with self.assertRaises(RecordNotFoundError):
            self.table._update(999, data)  # Non-existent ID

    def test_update_no_changes(self) -> None:
        """Test updating with no changes (valid fields only)."""
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("John Doe", 100.0),
        )
        self.connection.commit()

        data: dict[str, str] = {"name": "John Doe", "balance": "100.0"}
        self.table._update(1, data)  # No change, but should not raise an error

        result: list[dict[str, str]] = self.table.get_one(1)
        self.assertEqual(
            result, [{"id": 1, "name": "John Doe", "balance": 100.0}]
        )

    def test_delete_valid(self) -> None:
        """Test deleting an existing record."""
        self.cursor.execute(
            "INSERT INTO banks (name, balance) VALUES (?, ?)",
            ("John Doe", 100.0),
        )
        self.connection.commit()

        self.table._delete(1)

        with self.assertRaises(RecordNotFoundError):
            self.table.get_one(
                1
            )  # Should raise error because record is deleted

    def test_delete_not_found(self) -> None:
        """Test deleting a non-existent record."""
        with self.assertRaises(RecordNotFoundError):
            self.table._delete(999)  # Non-existent ID

    def test_column_mismatch(self) -> None:
        """Test column mismatch error when converting row to dict."""
        # Simulating a column mismatch by manually modifying row length
        row = sqlite3.Row(
            self.cursor, ("id", "name", "balance")
        )  # Use a tuple instead of a list
        with self.assertRaises(ColumnMismatchError):
            self.table._row_to_dict(
                row
            )  # This should raise ColumnMismatchError


if __name__ == "__main__":
    unittest.main()
