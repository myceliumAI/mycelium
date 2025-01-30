from typing import Any, Literal

from pydantic import Field

from .field import TemplateField


class SelectField(TemplateField):
    """Model for select input fields."""

    type: Literal["select"] = Field(
        "select",
        description="Type of the field",
        json_schema_extra={"example": "select"},
    )
    options: list[Any] = Field(
        ...,
        description="Options for select fields",
        json_schema_extra={"example": ["Option 1", "Option 2"]},
    )
