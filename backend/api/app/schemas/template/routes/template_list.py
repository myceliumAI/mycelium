from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.template import Template


class TemplateListResponse(BaseModelWithExample):
    """
    Represents the response for a successful template list retrieval.
    """

    message: str = Field(
        ...,
        json_schema_extra={"example": " ✅ Templates retrieved successfully"},
        description="A success message indicating the templates were retrieved.",
    )
    data: list[Template] = Field(
        ...,
        json_schema_extra={"example": Template.get_example()},
        description="The list of retrieved templates.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
