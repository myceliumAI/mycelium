from typing import Dict

from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from .tabs import TemplateTab


class Template(BaseModelWithExample):
    """Response model for a template."""

    id: str = Field(
        ...,
        description="Unique template identifier",
        example="mysql",
    )
    name: str = Field(
        ...,
        description="Template name",
        example="MySQL Database",
    )
    description: str = Field(
        "",
        description="Template description",
        example="Template for MySQL database connections",
    )

    tabs: Dict[str, TemplateTab] = Field(
        ...,
        description="List of tabs for the template",
        example={"info": TemplateTab.get_example()},
    )

    model_config = ConfigDict(populate_by_name=True)
