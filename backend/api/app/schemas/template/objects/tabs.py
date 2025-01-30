from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from .array_field import ArrayField
from .boolean_field import BooleanField
from .number_field import NumberField
from .password_field import PasswordField
from .select_field import SelectField
from .text_area_field import TextAreaField
from .text_field import TextField


class TemplateTab(BaseModelWithExample):
    """Response model for a template tab."""

    label: str = Field(
        ...,
        description="Label of the tab",
        json_schema_extra={"example": "Information"},
    )
    description: str = Field(
        ...,
        description="Description of the tab",
        json_schema_extra={"example": "Basic information about the data contract"},
    )
    fields: list[
        TextField
        | PasswordField
        | TextAreaField
        | NumberField
        | BooleanField
        | SelectField
        | ArrayField
    ] = Field(
        ...,
        description="List of fields for the tab",
        json_schema_extra={"example": [TextField.get_example()]},
    )
    model_config = ConfigDict(populate_by_name=True)
