"""Data Contract routes related error classes."""

from fastapi import HTTPException, status

from ..crud.data_contract import (
    DataContractNotFoundError,
    DataContractOperationError,
    DataContractValidationError,
)


def raise_not_found(id: str) -> None:
    """
    Raise HTTP 404 exception for not found data contract.

    :param str id: The ID of the data contract that was not found
    :raises HTTPException: 404 Not Found error with appropriate message
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=DataContractNotFoundError(id).message,
    )


def raise_invalid_schema(err: ValueError) -> None:
    """
    Raise HTTP 400 exception for invalid schema.

    :param ValueError err: The validation error that occurred
    :raises HTTPException: 400 Bad Request error with appropriate message
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=DataContractValidationError(str(err)).message,
    )


def raise_internal_error(err: Exception, operation: str) -> None:
    """
    Raise HTTP 500 exception for internal errors.

    :param Exception err: The error that occurred
    :param str operation: The operation that failed (create, update, delete, etc.)
    :raises HTTPException: 500 Internal Server Error with appropriate message
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=DataContractOperationError(operation).message,
    ) from err
