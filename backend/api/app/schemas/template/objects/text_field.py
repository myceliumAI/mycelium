from typing import Literal, Optional

from pydantic import Field

from .field import TemplateField


class TextField(TemplateField):
    """Model for text input fields."""

    type: Literal["text"] = Field(
        "text",
        description="Type of the field",
        example="text",
    )
    placeholder: str = Field(
        "",
        description="Placeholder text for the field",
        example="Enter title...",
    )
    pattern: Optional[str] = Field(
        None,
        description="Regex pattern for text validation",
        example="^\\d+\\.\\d+\\.\\d+$",
    )
