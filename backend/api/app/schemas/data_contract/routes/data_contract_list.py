from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractListResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract list retrieval.
    """

    message: str = Field(
        ...,
        json_schema_extra={"example": " ✅ Data contracts retrieved successfully"},
        description="A success message indicating the data contracts were retrieved.",
    )
    data: list[DataContract] = Field(
        ...,
        json_schema_extra={"example": DataContract.get_example()},
        description="The list of retrieved data contracts.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
