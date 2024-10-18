from pydantic import ConfigDict, Field

from ..data_contract.data_contract import DataContract
from ...utils.example_model import BaseModelWithExample

class DataContractCreate(DataContract):
    """
    Represents the input model for creating a new data contract.
    Inherits all fields from the base DataContract model.
    """
    pass


class DataContractCreateResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract creation.
    """

    message: str = Field(
        ...,
        example="✅ Data contract created successfully",
        description="A success message indicating the data contract was created.",
    )
    data: DataContract = Field(
        ...,
        example=DataContract.example(),
        description="The created data contract.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
