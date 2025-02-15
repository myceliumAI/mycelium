from typing import Literal

from pydantic import Field

from .field import TemplateField


class TextField(TemplateField):
    """Model for text input fields."""

    type: Literal["text"] = Field(
        "text",
        description="Type of the field",
        json_schema_extra={"example": "text"},
    )
    placeholder: str = Field(
        "",
        description="Placeholder text for the field",
        json_schema_extra={"example": "Enter title..."},
    )
    pattern: str | None = Field(
        None,
        description="Regex pattern for text validation",
        json_schema_extra={"example": "^\\d+\\.\\d+\\.\\d+$"},
    )
