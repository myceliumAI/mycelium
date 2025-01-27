"""Template routes related error classes."""

from fastapi import HTTPException, status

from ..crud.template import TemplateNotFoundError, TemplateOperationError


def raise_not_found(template_id: str) -> None:
    """
    Raise HTTP 404 exception for not found template.

    :param str template_id: The ID of the template that was not found
    :raises HTTPException: 404 Not Found error with appropriate message
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=TemplateNotFoundError(template_id).message,
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
        detail=TemplateOperationError(operation).message,
    ) from err
