from typing import Literal

from pydantic import Field

from .field import TemplateField


class PasswordField(TemplateField):
    """Model for password input fields."""

    type: Literal["password"] = Field(
        "password",
        description="Type of the field",
        example="password",
    )
    placeholder: str = Field(
        "",
        description="Placeholder text for the field",
        example="Enter password...",
    )
