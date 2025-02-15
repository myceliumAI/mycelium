from typing import Literal

from pydantic import Field

from .array_item import ArrayItem
from .field import TemplateField


class ArrayField(TemplateField):
    """Model for array input fields."""

    type: Literal["array"] = Field(
        ...,
        description="Type of the field",
        json_schema_extra={"example": "array"},
    )
    items: ArrayItem = Field(
        ...,
        description="Items of the array",
        json_schema_extra={"example": [ArrayItem.get_example()]},
    )
