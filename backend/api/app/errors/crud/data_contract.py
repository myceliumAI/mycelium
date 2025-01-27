"""Data Contract CRUD related error classes."""


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
