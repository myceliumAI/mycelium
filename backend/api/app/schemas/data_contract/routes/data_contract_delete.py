from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractDelete(BaseModelWithExample):
    """
    Represents the input model for deleting an existing data contract.
    """

    id: str = Field(
        ...,
        json_schema_extra={"example": "urn:datacontract:checkout:orders-latest"},
        description="The unique identifier of the data contract to delete.",
    )


class DataContractDeleteResponse(BaseModelWithExample):
    """
    Represents the API response for a data contract deletion.
    """

    message: str = Field(
        ...,
        json_schema_extra={"example": " ✅ Data contract deleted successfully"},
        description="A success message indicating the data contract was deleted.",
    )
    data: DataContract = Field(
        ...,
        json_schema_extra={"example": DataContract.get_example()},
        description="The deleted data contract information.",
    )
