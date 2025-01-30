from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample
from ..objects.data_contract import DataContract


class DataContractUpdate(DataContract):
    """
    Represents the input model for updating an existing data contract.
    All fields are optional to allow partial updates.
    """

    pass


class DataContractUpdateResponse(BaseModelWithExample):
    """
    Represents the response for a successful data contract update.

    :param str message: A success message indicating the data contract was updated.
    :param DataContract data: The updated data contract.
    """

    message: str = Field(
        ...,
        json_schema_extra={"example": " ✅ Data contract updated successfully"},
        description="A success message indicating the data contract was updated.",
    )
    data: DataContract = Field(
        ...,
        json_schema_extra={"example": DataContract.get_example()},
        description="The updated data contract.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)
