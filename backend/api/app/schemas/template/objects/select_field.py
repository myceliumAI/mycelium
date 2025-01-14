from typing import Any, List, Literal

from pydantic import Field

from .field import TemplateField


class SelectField(TemplateField):
    """Model for select input fields."""

    type: Literal["select"] = Field(
        "select",
        description="Type of the field",
        example="select",
    )
    options: List[Any] = Field(
        ...,
        description="Options for select fields",
        example=["Option 1", "Option 2"],
    )
