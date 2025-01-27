"""Data Contract CRUD related error classes."""

from sqlalchemy.exc import SQLAlchemyError


class DataContractCRUDError(Exception):
    """Base exception class for data contract CRUD operations."""

    pass


class DataContractNotFoundError(DataContractCRUDError):
    """Exception raised when a data contract is not found."""

    def __init__(self, contract_id: str):
        self.message = f" ❌ Data contract with id '{contract_id}' not found"
        super().__init__(self.message)


class DataContractOperationError(DataContractCRUDError):
    """Exception raised when a data contract operation fails."""

    def __init__(self, operation: str):
        self.message = f" ❌ Failed to {operation} data contract"
        super().__init__(self.message)


class DataContractValidationError(DataContractCRUDError):
    """Exception raised when data contract validation fails."""

    def __init__(self, message: str):
        self.message = f" ❌ Invalid data contract schema: {message}"
        super().__init__(self.message)


def raise_not_found_error(id: str) -> None:
    """
    Handle not found errors by raising an appropriate exception.

    :param str id: The ID of the data contract that was not found
    :raises DataContractNotFoundError: With appropriate error message
    """
    raise DataContractNotFoundError(id)


def raise_sqlalchemy_error(error: SQLAlchemyError, operation: str) -> None:
    """
    Handle SQLAlchemy errors by raising an appropriate exception.

    :param SQLAlchemyError error: The SQLAlchemy error that occurred
    :param str operation: The operation that failed (create, update, delete, etc.)
    :raises DataContractOperationError: With appropriate error message
    """
    raise DataContractOperationError(operation) from error
