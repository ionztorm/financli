import sqlite3
import unittest

from pathlib import Path

from features.banks.model import Bank
from features.banks.schema import CREATE_BANKS_TABLE

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
TEST_DB_PATH = DATA_DIR / "test.db"


class TestBankModel(unittest.TestCase):
    conn: sqlite3.Connection
    bank: Bank

    @classmethod
    def setUpClass(cls) -> None:
        DATA_DIR.mkdir(exist_ok=True)
        cls.conn = sqlite3.connect(TEST_DB_PATH)
        cls.conn.execute("DROP TABLE IF EXISTS banks")
        cls.conn.execute(CREATE_BANKS_TABLE)
        cls.conn.commit()
        cls.bank = Bank(cls.conn)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()

    def test_open_account(self) -> None:
        self.bank.open({"name": "Test Account", "balance": "100"})
        accounts = self.bank.get_many()
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["name"], "Test Account")
        self.assertEqual(accounts[0]["balance"], "100")

    def test_close_account(self) -> None:
        self.bank.open({"name": "To Close", "balance": "0"})
        accounts = self.bank.get_many()
        account_id = int(accounts[-1]["id"])
        self.bank.close(account_id)

        remaining = self.bank.get_many()
        self.assertNotIn(account_id, [int(acc["id"]) for acc in remaining])


if __name__ == "__main__":
    unittest.main()
