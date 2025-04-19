import sqlite3
import unittest

from core.db.init import (
    DB_PATH,
    get_connection,
    create_data_path,
)


class TestDatabaseSetup(unittest.TestCase):
    conn: sqlite3.Connection

    @classmethod
    def setUpClass(cls) -> None:
        create_data_path()
        cls.conn = get_connection()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()

    def test_data_directory_exists(self) -> None:
        self.assertTrue(DB_PATH.parent.exists(), "Data directory should exist")

    def test_database_file_created(self) -> None:
        self.assertTrue(
            DB_PATH.exists(), "Database file should exist after connection"
        )

    def test_required_tables_exist(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}

        expected_tables = {"banks", "transactions"}
        for table in expected_tables:
            self.assertIn(table, tables, f"Table '{table}' should exist")


if __name__ == "__main__":
    unittest.main()
