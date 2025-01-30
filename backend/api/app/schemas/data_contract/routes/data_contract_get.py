from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractGetResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract retrieval.
    """

    message: str = Field(
        ...,
        json_schema_extra={"example": " ✅ Data contract retrieved successfully"},
        description="A success message indicating the data contract was retrieved.",
    )
    data: DataContract = Field(
        ...,
        json_schema_extra={"example": DataContract.get_example()},
        description="The retrieved data contract.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
