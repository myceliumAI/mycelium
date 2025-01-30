from typing import Any

from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample


class TemplateField(BaseModelWithExample):
    """Base model for all template fields."""

    name: str = Field(
        ...,
        description="Name of the field",
        json_schema_extra={"example": "title"},
    )
    label: str = Field(
        ...,
        description="Label of the field",
        json_schema_extra={"example": "Title"},
    )
    required: bool = Field(
        False,
        description="Whether the field is required",
        json_schema_extra={"example": True},
    )
    hint: str = Field(
        "",
        description="Hint for the field",
        json_schema_extra={"example": "A descriptive name for this data contract"},
    )
    default: Any | None = Field(
        None,
        description="Default value for the field",
        json_schema_extra={"example": "My Data Contract"},
    )

    model_config = ConfigDict(populate_by_name=True)
