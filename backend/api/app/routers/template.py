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

router = APIRouter(prefix="/templates", tags=["templates"])
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

def validate_template_id(template_id: str) -> bool:
    """
    Validates a template identifier using werkzeug's secure_filename.
    
    Args:
        template_id: The identifier to validate

    Returns:
        bool: True if the identifier is valid, False otherwise
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

    Args:
        template_path: Path to the template file

    Returns:
        dict: Template content

    Raises:
        TemplateError: If the template cannot be loaded
    """
    try:
        return yaml.safe_load(template_path.read_text())
    except Exception as e:
        raise TemplateError(f"Error loading template: {str(e)}")

def get_template_path(template_id: str) -> Path:
    """
    Safely constructs and validates a template path.
    
    Args:
        template_id: The template identifier
        
    Returns:
        Path: The validated template path
        
    Raises:
        HTTPException: If the path is invalid or unsafe
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
    summary="List all available templates",
    response_description="List of templates with their metadata"
)
async def list_templates() -> TemplateListResponse:
    """
    Retrieves the list of all available templates.
    Creates the templates directory if it doesn't exist.

    Returns:
        TemplateListResponse: List of available templates

    Raises:
        HTTPException: If an error occurs while loading templates
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
    summary="Retrieve a specific template",
    response_description="Complete template configuration"
)
async def get_template(template_id: str) -> dict:
    """
    Retrieves the configuration for a specific template.
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
