"""Database DSN related error classes."""


class DSNError(Exception):
    """Base exception class for DSN configuration errors."""

    pass


class MissingCredentialsError(DSNError):
    """Exception raised when required credentials are missing."""

    def __init__(self, missing_fields: list[str]):
        self.message = f"Missing required credentials: {', '.join(missing_fields)}"
        super().__init__(self.message)


class ConnectionMethodError(DSNError):
    """Exception raised when no valid connection method is provided."""

    def __init__(self):
        self.message = "Connection method required: either unix_socket or (host AND port)"
        super().__init__(self.message)
