from typing import Literal

from pydantic import Field

from .field import TemplateField


class TextAreaField(TemplateField):
    """Model for textarea input fields."""

    type: Literal["textarea"] = Field(
        "textarea",
        description="Type of the field",
        example="textarea",
    )
    placeholder: str = Field(
        "",
        description="Placeholder text for the field",
        example="Enter description...",
    )
    rows: int = Field(
        4,
        description="Number of rows for textarea fields",
        example=4,
    )
