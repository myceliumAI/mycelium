"""
Template management module for the API.
Responsible for reading and validating configuration templates.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from werkzeug.utils import secure_filename

from ..utils.logger import get_logger
from ..utils.exceptions import TemplateError

# Constants
TEMPLATE_FILE_SUFFIX = '.yaml'
ALLOWED_EXTENSIONS = {'yaml', 'yml'}

router = APIRouter()
logger = get_logger(__name__)

# Using Path for better path management
TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"

class TemplateNotFoundError(TemplateError):
    """Exception raised when a template is not found."""
    pass

class TemplateResponse(BaseModel):
    """Response model for a template."""
    id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field("", description="Template description")

class TemplateListResponse(BaseModel):
    """Response model for template listing."""
    templates: List[TemplateResponse] = Field(default_factory=list)

    @staticmethod
    def get_example():
        return {
            "templates": [
                {
                    "id": "mysql",
                    "name": "MySQL Database",
                    "description": "Template for MySQL database connections"
                },
                {
                    "id": "sftp",
                    "name": "SFTP Server",
                    "description": "Template for SFTP file transfers"
                }
            ]
        }

def validate_template_id(template_id: str) -> bool:
    """
    Validates a template identifier using werkzeug's secure_filename.

    This function checks if a given template identifier is valid by ensuring it meets
    security requirements and naming conventions.

    :param str template_id: The identifier to validate
    :return bool: True if the identifier is valid, False otherwise
    """
    secured_name = secure_filename(template_id)
    return (
        secured_name == template_id and  # Ensures the name hasn't been modified by secure_filename
        '.' not in template_id and       # Prevents any file extension in the ID
        template_id != ''                # Ensures non-empty ID
    )

def load_template_file(template_path: Path) -> dict:
    """
    Loads and parses a template file.

    This function reads a YAML template file from the given path and returns its contents
    as a dictionary. If the file cannot be loaded or parsed, it raises a TemplateError.

    :param Path template_path: Path to the template file
    :return dict: Template content as a dictionary
    :raises TemplateError: If the template cannot be loaded or parsed
    """
    try:
        return yaml.safe_load(template_path.read_text())
    except Exception as e:
        raise TemplateError(f"Error loading template: {str(e)}")

def get_template_path(template_id: str) -> Path:
    """
    Safely constructs and validates a template path.

    This function takes a template identifier and constructs a safe file path,
    ensuring that the resulting path is within the allowed templates directory
    and follows security best practices.

    :param str template_id: The template identifier
    :return Path: The validated template path
    :raises HTTPException:
        - 400 Bad Request: If the template identifier format is invalid
        - 400 Bad Request: If the resulting path is invalid or unsafe
    """
    safe_template_id = secure_filename(template_id)
    if not safe_template_id or safe_template_id != template_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid template identifier format"
        )

    template_path = TEMPLATES_DIR / f"{safe_template_id}{TEMPLATE_FILE_SUFFIX}"
    
    try:
        real_path = template_path.resolve()
        if not str(real_path).startswith(str(TEMPLATES_DIR.resolve())):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid template path"
            )
        return real_path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid template path"
        )

@router.get(
    "",
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
                    "example": {"detail": "❌ Internal error while loading templates"}
                }
            },
        },
    },
    tags=["templates"],
)
async def list_templates() -> TemplateListResponse:
    """
    Retrieves the list of all available templates.

    This endpoint scans the templates directory, loads each valid template file,
    and returns a list of template metadata. It creates the templates directory
    if it doesn't exist.

    :return TemplateListResponse: List of available templates with their metadata
    :raises HTTPException:
        - 500 Internal Server Error: If an error occurs while loading templates
    """
    try:
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        
        templates = []
        for template_file in TEMPLATES_DIR.glob(f"*{TEMPLATE_FILE_SUFFIX}"):
            template_id = template_file.stem
            
            if not validate_template_id(template_id):
                logger.warning(f"Skipped template - Invalid ID: {template_id}")
                continue

            try:
                template_data = load_template_file(template_file)
                templates.append(
                    TemplateResponse(
                        id=template_id,
                        name=template_data.get("name", template_id),
                        description=template_data.get("description", "")
                    )
                )
            except TemplateError as e:
                logger.error(f"Template error {template_id}: {str(e)}")
                continue

        logger.info(f"Found templates: {len(templates)}")
        return TemplateListResponse(templates=templates)

    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error while loading templates"
        )

@router.get(
    "/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a specific template",
    description="Retrieves the complete configuration for a specific template by its identifier.",
    response_description="Complete template configuration",
    responses={
        200: {
            "description": "Successfully retrieved template",
            "content": {
                "application/json": {
                    "example": {
                        "name": "MySQL Database",
                        "description": "Template for MySQL database connections",
                        "fields": {
                            "host": {"type": "string", "required": True},
                            "port": {"type": "integer", "default": 3306},
                            "database": {"type": "string", "required": True},
                            "username": {"type": "string", "required": True},
                            "password": {"type": "string", "required": True, "secret": True}
                        }
                    }
                }
            },
        },
        400: {
            "description": "Invalid template identifier",
            "content": {
                "application/json": {
                    "example": {"detail": "❌ Invalid template identifier format"}
                }
            },
        },
        404: {
            "description": "Template not found",
            "content": {
                "application/json": {
                    "example": {"detail": "❌ Template not found"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "❌ Error loading template: Invalid YAML format"}
                }
            },
        },
    },
    tags=["templates"],
)
async def get_template(template_id: str) -> dict:
    """
    Retrieves the configuration for a specific template.

    This endpoint loads and returns the complete configuration for a requested template.
    It validates the template identifier and ensures the template file exists before
    attempting to load it.

    :param str template_id: The identifier of the template to retrieve
    :return dict: Complete template configuration
    :raises HTTPException:
        - 404 Not Found: If the requested template doesn't exist
        - 400 Bad Request: If the template identifier is invalid
        - 500 Internal Server Error: If the template cannot be loaded
    """
    template_path = get_template_path(template_id)

    if not template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found"
        )

    try:
        return load_template_file(template_path)
    except TemplateError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
