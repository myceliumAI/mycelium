from typing import Literal

from pydantic import Field

from .field import TemplateField


class BooleanField(TemplateField):
    """Model for boolean input fields."""

    type: Literal["boolean"] = Field(
        "boolean",
        description="Type of the field",
        json_schema_extra={"example": "boolean"},
    )
