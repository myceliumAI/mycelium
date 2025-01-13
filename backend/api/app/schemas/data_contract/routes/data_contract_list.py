from typing import List

from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractListResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract list retrieval.
    """

    message: str = Field(
        ...,
        example=" ✅ Data contracts retrieved successfully",
        description="A success message indicating the data contracts were retrieved.",
    )
    data: List[DataContract] = Field(
        ...,
        example=DataContract.get_example(),
        description="The list of retrieved data contracts.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
