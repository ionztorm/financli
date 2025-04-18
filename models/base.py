import sqlite3

from utils.types import TableName
from utils.helpers import msg


class Table:
    def __init__(
        self, connection: sqlite3.Connection, table: TableName
    ) -> None:
        self._connection = connection
        self._cursor = connection.cursor()
        self._table = table

        self._cursor.execute(f"PRAGMA table_info({self._table.value})")
        self.columns = self._cursor.fetchall()
        self.insert_cols = [row[1] for row in self.columns if row[1] != "id"]
        self.required_fields = [col[1] for col in self.columns if col[3] == 1]

    def get_one(self, id: int) -> list[dict[str, str]]:
        try:
            self._cursor.execute(
                f"SELECT * FROM {self._table.value} WHERE id = ?",  # noqa: S608
                (id,),
            )
            row = self._cursor.fetchone()
            result = self.row_to_dict(row) if row else None

            if not result:
                return []
            return [result]
        except ValueError as e:
            msg(f"Error: {e}")
            return []

    def get_many(self) -> list[dict[str, str]]:
        try:
            self._cursor.execute(f"SELECT * FROM {self._table.value}")  # noqa: S608
            rows = self._cursor.fetchall()
            return [self.row_to_dict(row) for row in rows]
        except ValueError as e:
            msg(f"Error: {e}")
            return []

    def create(self, data: dict) -> bool:
        if not self.validate_data(data):
            return False

        placeholders = ", ".join("?" for _ in self.insert_cols)
        col_list = ", ".join(self.insert_cols)
        values = tuple(data.get(col) for col in self.insert_cols)
        query = (
            f"INSERT INTO {self._table.value} ({col_list}) "
            f"VALUES({placeholders})"
        )

        result = self.execute_query(query, values)

        if result:
            self._connection.commit()
            return True
        return False

    def update(self, id: int, data: dict) -> bool:
        if not self.exists(id):
            return False

        update_columns = [col for col in data.keys() if col in self.insert_cols]
        assignments = ", ".join(f"{col} = ?" for col in self.insert_cols)
        current = self.get_one(id)

        if not current:
            msg(f"No item found with an id {id}")
            return False

        values = tuple(
            data[col] if data[col] is not None else current[col]
            for col in update_columns
        )
        query = f"UPDATE {self._table.value} SET {assignments} WHERE id = ?"  # noqa: S608

        result = self.execute_query(query, (*values, id))

        if result:
            self._connection.commit()
            return True
        return False

    def delete(self, id: int) -> bool:
        if not self.exists(id):
            return False

        query = f"DELETE FROM {self._table.value} WHERE id = ?"  # noqa: S608
        result = self.execute_query(query, (id,))

        if result:
            self._connection.commit()
            return True
        return False

    def row_to_dict(self, row: sqlite3.Row) -> dict[str, str]:
        column_names = [column[0] for column in self._cursor.description]
        if len(column_names) != len(row):
            raise ValueError(
                f"Column mismatch: expected {len(column_names)} columns, "
                f"got {len(row)}"
            )
        return dict(zip(column_names, row))

    def exists(self, id: int) -> bool:
        self._cursor.execute(
            f"SELECT 1 FROM {self._table.value} WHERE id = ?",  # noqa: S608
            (id,),
        )
        return self._cursor.fetchone() is not None

    def validate_data(self, data: dict[str, str]) -> bool:
        missing_fields = [
            field
            for field in self.required_fields
            if field not in data or data[field] is None
        ]
        if missing_fields:
            msg("Error: The following required fields are required: ")
            for field in missing_fields:
                print(f" - {field}")
            return False

        return True

    def execute_query(
        self, query: str, params: tuple = ()
    ) -> sqlite3.Cursor | None:
        try:
            self._cursor.execute(query, params)
        except sqlite3.Error as e:
            msg(f"Database error: {e}")
            return None
        return self._cursor
