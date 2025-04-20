import sqlite3

from utils.types import TableName
from utils.helpers import wrap_error
from core.exceptions import (
    ValidationError,
    ColumnMismatchError,
    QueryExecutionError,
    RecordNotFoundError,
)


class Table:
    def __init__(
        self, connection: sqlite3.Connection, table_name: TableName
    ) -> None:
        self._connection = connection
        self._cursor = connection.cursor()
        self._table_name = table_name

        self._cursor.execute(f"PRAGMA table_info({self._table_name.value})")
        self.table_schema = self._cursor.fetchall()
        self.table_columns = [
            row[1] for row in self.table_schema if row[1] != "id"
        ]
        self.required_columns = [
            col[1] for col in self.table_schema if col[3] == 1
        ]

    def get_one(self, id: int) -> list[dict[str, str]]:
        try:
            self._cursor.execute(
                f"SELECT * FROM {self._table_name.value} WHERE id = ?",  # noqa: S608
                (id,),
            )
            row = self._cursor.fetchone()
            if not row:
                raise RecordNotFoundError(f"No record found with ID {id}.")
            return [self._row_to_dict(row)]
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Failed to fetch record")
            raise wrapper(e) from e

    def get_many(self) -> list[dict[str, str]]:
        try:
            self._cursor.execute(f"SELECT * FROM {self._table_name.value}")  # noqa: S608
            rows = self._cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Failed to fetch records")
            raise wrapper(e) from e

    def _create(self, data: dict[str, str]) -> None:
        self._validate_data(data)

        placeholders = ", ".join("?" for _ in self.table_columns)
        col_list = ", ".join(self.table_columns)
        values = tuple(data.get(col) for col in self.table_columns)
        query = (
            f"INSERT INTO {self._table_name.value} ({col_list}) "
            f"VALUES({placeholders})"
        )

        try:
            self._execute_query(query, values)
            self._connection.commit()
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Failed to create record")
            raise wrapper(e) from e

    def exists(self, id: int) -> bool:
        try:
            self._cursor.execute(
                f"SELECT 1 FROM {self._table_name.value} WHERE id = ?",  # noqa: S608
                (id,),
            )
            return self._cursor.fetchone() is not None
        except sqlite3.Error as e:
            wrapper = wrap_error(
                QueryExecutionError, "Failed to check record existence"
            )
            raise wrapper(e) from e

    def _update(self, id: int, data: dict[str, str]) -> None:
        if not self.exists(id):
            raise RecordNotFoundError(f"Record with ID {id} does not exist.")

        update_columns = [
            col for col in data.keys() if col in self.table_columns
        ]
        if not update_columns:
            raise ValidationError("No valid fields to update.")

        current = self.get_one(id)

        values = tuple(
            data[col] if data[col] is not None else current[0][col]
            for col in update_columns
        )
        assignments = ", ".join(f"{col} = ?" for col in update_columns)
        query = (
            f"UPDATE {self._table_name.value} SET {assignments} WHERE id = ?"  # noqa: S608
        )

        try:
            self._execute_query(query, (*values, id))
            self._connection.commit()
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Failed to update record")
            raise wrapper(e) from e

    def _delete(self, id: int) -> None:
        if not self.exists(id):
            raise RecordNotFoundError(
                f"Cannot delete: record with ID {id} does not exist."
            )

        query = f"DELETE FROM {self._table_name.value} WHERE id = ?"  # noqa: S608
        try:
            self._execute_query(query, (id,))
            self._connection.commit()
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Failed to delete record")
            raise wrapper(e) from e

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, str]:
        column_names = [column[0] for column in self._cursor.description]
        if len(column_names) != len(row):
            raise ColumnMismatchError(
                f"Column mismatch: expected {len(column_names)} columns, "
                f"got {len(row)}"
            )
        return dict(zip(column_names, row))

    def _validate_data(self, data: dict[str, str]) -> None:
        missing_fields = [
            field
            for field in self.required_columns
            if field not in data or data[field] is None
        ]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    def _execute_query(self, query: str, params: tuple = ()) -> None:
        try:
            self._cursor.execute(query, params)
        except sqlite3.Error as e:
            wrapper = wrap_error(QueryExecutionError, "Database error")
            raise wrapper(e) from e

    def _get_balance(self, id: int) -> float:
        record = self.get_one(id)
        balance = record[0].get("balance")
        return float(balance) if balance is not None else 0.0
