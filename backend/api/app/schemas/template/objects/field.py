from typing import Any, Optional

from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample


class TemplateField(BaseModelWithExample):
    """Base model for all template fields."""

    name: str = Field(
        ...,
        description="Name of the field",
        example="title",
    )
    label: str = Field(
        ...,
        description="Label of the field",
        example="Title",
    )
    required: bool = Field(
        False,
        description="Whether the field is required",
        example=True,
    )
    hint: str = Field(
        "",
        description="Hint for the field",
        example="A descriptive name for this data contract",
    )
    default: Optional[Any] = Field(
        None,
        description="Default value for the field",
        example="My Data Contract",
    )

    model_config = ConfigDict(populate_by_name=True)
