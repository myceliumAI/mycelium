"""Database manager related error classes."""


class DatabaseError(Exception):
    """Base exception class for database errors."""

    pass


class DatabaseInitializationError(DatabaseError):
    """Exception raised when database engine is not initialized."""

    def __init__(self):
        self.message = " ❌ Database engine not initialized. Call setup_engine() first."
        super().__init__(self.message)


class UnsupportedDatabaseError(DatabaseError):
    """Exception raised when an unsupported database type is used."""

    def __init__(self):
        self.message = " ❌ Only PostgreSQL databases are supported"
        super().__init__(self.message)
