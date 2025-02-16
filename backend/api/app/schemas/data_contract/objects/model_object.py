from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from .config_object import ConfigObject
from .field_object import FieldObject


class ModelObject(BaseModelWithExample):
    """
    Represents a model object in a data contract.

    This class defines the structure and properties of a data model,
    such as tables, views, or structured files.
    """

    type: str = Field(
        default="table",
        description="The type of the model. Examples: table, view, object.",
        json_schema_extra={"example": "table"},
    )
    description: str | None = Field(
        None,
        description="An optional string describing the data model.",
        json_schema_extra={
            "example": "One record per order. Includes cancelled and deleted orders."
        },
    )
    title: str | None = Field(
        None,
        description="An optional string for the title of the data model. "
        "Especially useful if the name of the model is cryptic or contains abbreviations.",
        json_schema_extra={"example": "Orders Latest"},
    )
    fields: dict[str, FieldObject] = Field(
        ...,
        description="The fields (e.g. columns) of the data model.",
        json_schema_extra={
            "example": {
                "order_id": FieldObject(
                    description="Unique identifier for the order",
                    type="string",
                    format="uuid",
                    required=True,
                    unique=True,
                    primary=True,
                    example="243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
                ),
                "order_timestamp": FieldObject(
                    description="Timestamp of the order",
                    type="timestamp",
                    required=True,
                    example="2024-09-09T08:30:00Z",
                ),
            }
        },
    )
    config: ConfigObject | None = Field(
        None,
        description="Any additional key-value pairs that might be useful for further tooling.",
        json_schema_extra={"example": ConfigObject.get_example()},
    )
