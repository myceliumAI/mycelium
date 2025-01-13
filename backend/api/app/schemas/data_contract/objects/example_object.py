from typing import Optional

from pydantic import Field

from ....utils.example_model import BaseModelWithExample


class ExampleObject(BaseModelWithExample):
    """
    Represents an example object in a data contract.

    This class defines the structure and properties of an example,
    including its type, data, description, and associated model.
    """

    type: str = Field(
        ...,
        description="The type of the data product technology that implements the data contract.",
        example="csv",
    )
    description: Optional[str] = Field(
        None,
        description="An optional string describing the example.",
        example="An example list of order records.",
    )
    model: str = Field(
        ...,
        description="The reference to the model in the schema, e.g. a table name.",
        example="orders",
    )
    data: str = Field(
        ...,
        description="Example data for this model.",
        example="order_id,order_timestamp,order_total\n" '"1001","2023-09-09T08:30:00Z",2500\n',
    )
