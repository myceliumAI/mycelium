from typing import Literal

from pydantic import Field

from .field import TemplateField


class NumberField(TemplateField):
    """Model for number input fields."""

    type: Literal["number"] = Field(
        "number",
        description="Type of the field",
        example="number",
    )
    min: float = Field(
        None,
        description="Minimum value for number fields",
        example=1,
    )
    max: float = Field(
        None,
        description="Maximum value for number fields",
        example=100,
    )
    step: float = Field(
        1,
        description="Step value for number fields",
        example=0.1,
    )
