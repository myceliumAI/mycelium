from typing import TYPE_CHECKING, Literal, Union

from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from .boolean_field import BooleanField
from .number_field import NumberField
from .password_field import PasswordField
from .select_field import SelectField
from .text_area_field import TextAreaField
from .text_field import TextField


if TYPE_CHECKING:
    from .array_field import ArrayField


class ArrayItem(BaseModelWithExample):
    """Model for array input fields that contain nested properties."""

    type: Literal["object"] = Field(
        "object",
        description="Type of the field",
        example="object",
    )
    properties: list[
        Union[
            TextField,
            PasswordField,
            TextAreaField,
            NumberField,
            BooleanField,
            SelectField,
            "ArrayField",
        ]
    ] = Field(
        ...,
        description="List of nested field properties",
        example=[TextField.get_example()],
    )
