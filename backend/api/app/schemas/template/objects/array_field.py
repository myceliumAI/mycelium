from typing import Literal

from pydantic import Field

from .field import TemplateField
from .object_field import ObjectField


class ArrayField(TemplateField):
    """Model for array input fields."""

    type: Literal["array"] = Field(
        "array",
        description="Type of the field",
        example="array",
    )
    items: ObjectField = Field(
        ...,
        description="Items of the array",
        example=[ObjectField.get_example()],
    )
