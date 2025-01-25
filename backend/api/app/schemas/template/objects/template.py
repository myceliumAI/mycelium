from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from .array_field import ArrayField
from .tabs import TemplateTab


class Template(BaseModelWithExample):
    """Response model for a template."""

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
    tabs: dict[str, TemplateTab] = Field(
        ...,
        description="List of tabs for the template",
        example={"info": TemplateTab.get_example(), "schema": ArrayField.get_example()},
    )
    id: str = Field(
        ...,
        description="Unique template identifier",
        example="mysql",
    )

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
