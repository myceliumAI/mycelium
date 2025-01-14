from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.template import Template


class TemplateGetResponse(BaseModelWithExample):
    """
    Represents the response for a successful template retrieval.
    """

    message: str = Field(
        ...,
        example=" ✅ Template retrieved successfully",
        description="A success message indicating the template was retrieved.",
    )
    data: Template = Field(
        ...,
        example=Template.get_example(),
        description="The retrieved template.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
