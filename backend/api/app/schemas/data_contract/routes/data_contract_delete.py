from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractDelete(BaseModelWithExample):
    """
    Represents the input model for deleting an existing data contract.
    """

    id: str = Field(
        ...,
        example="urn:datacontract:checkout:orders-latest",
        description="The unique identifier of the data contract to delete.",
    )


class DataContractDeleteResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract deletion.
    """

    message: str = Field(
        ...,
        example=" ✅ Data contract deleted successfully",
        description="A success message indicating the data contract was deleted.",
    )
    data: DataContract = Field(
        ...,
        example=DataContract.get_example(),
        description="The deleted data contract information.",
    )
