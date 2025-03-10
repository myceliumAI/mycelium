"""
Template management module for the API.
Responsible for reading and validating configuration templates.
"""

from fastapi import APIRouter, status

from ..exceptions.routers.template import raise_internal_error, raise_not_found
from ..schemas.template.routes.template_get import TemplateGetResponse
from ..schemas.template.routes.template_list import TemplateListResponse
from ..services.template import template_service
from ..utils.logger import get_logger


router = APIRouter(tags=["Template"])
logger = get_logger(__name__)


@router.get(
    "/",
    response_model=TemplateListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all available templates",
    description="Retrieves a list of all available configuration templates with their metadata.",
    response_description="List of templates with their metadata",
    responses={
        200: {
            "description": "Successfully retrieved templates",
            "content": {"application/json": {"example": TemplateListResponse.get_example()}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to retrieve templates: Internal server error"}
                }
            },
        },
    },
)
async def list_templates_route() -> TemplateListResponse:
    """
    Retrieves all templates.

    This endpoint attempts to retrieve all templates using the template service.
    If successful, it returns a list of all templates.
    If an error occurs during the process, it raises an appropriate HTTP exception.

    :return TemplateListResponse: A response containing a success message and the list of templates.
    :raises HTTPException:
        - 500 Internal Server Error: If there's an unexpected error during template retrieval.
    """
    try:
        templates = template_service.list_templates()
        return TemplateListResponse(message=" ✅ Templates retrieved successfully", data=templates)
    except Exception as e:
        raise_internal_error(e, "retrieve")


@router.get(
    "/{template_id}",
    response_model=TemplateGetResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific template",
    description="Retrieves a specific template by its identifier.",
    response_description="Complete template configuration",
    responses={
        200: {
            "description": "Successfully retrieved template",
            "content": {"application/json": {"example": TemplateGetResponse.get_example()}},
        },
        404: {
            "description": "Template not found",
            "content": {"application/json": {"example": {"detail": " ❌ Template not found"}}},
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": " ❌ Failed to retrieve template: Internal server error"}
                }
            },
        },
    },
)
async def get_template_route(template_id: str) -> TemplateGetResponse:
    """
    Retrieves a specific template by its ID.

    This endpoint accepts a template ID, attempts to retrieve the corresponding
    template using the template service. If successful, it returns the retrieved template.
    If the template is not found or an error occurs, it raises an appropriate HTTP exception.

    :param str template_id: The unique identifier of the template to retrieve.
    :return TemplateGetResponse: A response containing a success message and the retrieved template.
    :raises HTTPException:
        - 404 Not Found: If the template with the given ID is not found.
        - 500 Internal Server Error: If there's an unexpected error during template retrieval.
    """
    try:
        template = template_service.get_template(template_id)
        if template is None:
            raise_not_found(template_id)
        return TemplateGetResponse(message=" ✅ Template retrieved successfully", data=template)
    except Exception as e:
        raise_internal_error(e, "retrieve")
