from typing import List, Literal

from pydantic import Field

from .field import TemplateField
from .text_field import TextField


class ObjectField(TemplateField):
    """Model for object input fields that contain nested properties."""

    type: Literal["object"] = Field(
        "object",
        description="Type of the field",
        example="object",
    )
    properties: List[TemplateField] = Field(
        ...,
        description="List of nested field properties",
        example=[TextField.get_example()],
    )
