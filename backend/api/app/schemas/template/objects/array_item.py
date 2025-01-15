from typing import List, Literal, Union

from pydantic import Field

from .array_field import ArrayField
from .boolean_field import BooleanField
from .field import TemplateField
from .number_field import NumberField
from .password_field import PasswordField
from .select_field import SelectField
from .text_area_field import TextAreaField
from .text_field import TextField


class ArrayItem(TemplateField):
    """Model for array input fields that contain nested properties."""

    type: Literal["object"] = Field(
        "object",
        description="Type of the field",
        example="object",
    )
    properties: List[
        Union[
            TextField,
            PasswordField,
            TextAreaField,
            NumberField,
            BooleanField,
            SelectField,
            ArrayField,
        ]
    ] = Field(
        ...,
        description="List of nested field properties",
        example=[TextField.get_example()],
    )
