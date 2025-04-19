class DatabaseError(Exception):
    """Base exception for database-related operations."""


class RecordNotFoundError(DatabaseError):
    pass


class ValidationError(DatabaseError):
    pass


class QueryExecutionError(DatabaseError):
    pass


class ColumnMismatchError(DatabaseError):
    pass
