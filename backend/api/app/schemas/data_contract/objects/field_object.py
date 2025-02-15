from typing import Any, Optional

from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from .config_object import ConfigObject
from .data_type import DataType


class FieldObject(BaseModelWithExample):
    """
    Represents a field object in a data contract model.

    This class defines the structure and properties of a field,
    including its description, type, requirements, uniqueness, and sensitivity.
    """

    description: str | None = Field(
        None,
        description="An optional string describing the semantic of the data in this field.",
        json_schema_extra={"example": "Unique identifier for the order"},
    )
    type: DataType = Field(
        ...,
        description="The logical data type of the field.",
        json_schema_extra={"example": DataType.TEXT},
    )
    title: str | None = Field(
        None,
        description="An optional string providing a human readable name for the field. "
        "Especially useful if the field name is cryptic or contains abbreviations.",
        json_schema_extra={"example": "Order ID"},
    )
    enum: list[str] | None = Field(
        None,
        description="A value must be equal to one of the elements in this array value. "
        "Only evaluated if the value is not null.",
        json_schema_extra={"example": ["pending", "processing", "completed", "cancelled"]},
    )
    required: bool | None = Field(
        False,
        description="An indication, if this field must contain a value and may not be null.",
        json_schema_extra={"example": True},
    )
    primary: bool | None = Field(
        False,
        description="If this field is a primary key.",
        json_schema_extra={"example": True},
    )
    references: str | None = Field(
        None,
        description="The reference to a field in another model. E.g. use 'orders.order_id' "
        "to reference the order_id field of the model orders.",
        json_schema_extra={"example": "orders.order_id"},
    )
    unique: bool | None = Field(
        False,
        description="An indication, if the value must be unique within the model.",
        json_schema_extra={"example": True},
    )
    format: str | None = Field(
        None,
        description="Specifies the format of the field (e.g., email, uri, uuid).",
        json_schema_extra={"example": "uuid"},
    )
    precision: int | None = Field(
        None,
        description="The maximum number of digits in a number. Only applies to numeric values.",
        json_schema_extra={"example": 10},
    )
    scale: int | None = Field(
        None,
        description="The maximum number of decimal places in a number. Only applies to numeric values.",
        json_schema_extra={"example": 2},
    )
    min_length: int | None = Field(
        None,
        description="A value must be greater than, or equal to, the value of this. "
        "Only applies to unicode character sequences types.",
        json_schema_extra={"example": 10},
    )
    max_length: int | None = Field(
        None,
        description="A value must be less than, or equal to, the value of this. "
        "Only applies to unicode character sequences types.",
        json_schema_extra={"example": 20},
    )
    pattern: str | None = Field(
        None,
        description="A value must be valid according to the ECMA-262 regular expression dialect. "
        "Only applies to unicode character sequences types.",
        json_schema_extra={"example": "^[A-Za-z0-9]{8,14}$"},
    )
    minimum: float | None = Field(
        None,
        description="A value of a number must be greater than, or equal to, the value of this. "
        "Only applies to numeric values.",
        json_schema_extra={"example": 0},
    )
    exclusive_minimum: float | None = Field(
        None,
        description="A value of a number must be greater than the value of this. "
        "Only applies to numeric values.",
        json_schema_extra={"example": 0},
    )
    maximum: float | None = Field(
        None,
        description="A value of a number must be less than, or equal to, the value of this. "
        "Only applies to numeric values.",
        json_schema_extra={"example": 1000000},
    )
    exclusive_maximum: float | None = Field(
        None,
        description="A value of a number must be less than the value of this. "
        "Only applies to numeric values.",
        json_schema_extra={"example": 1000000},
    )
    example: Any | None = Field(
        None,
        description="An example value.",
        json_schema_extra={"example": "243c25e5-a081-43a9-aeab-6d5d5b6cb5e2"},
    )
    pii: bool | None = Field(
        None,
        description="An indication, if this field contains Personal Identifiable Information (PII).",
        json_schema_extra={"example": True},
    )
    classification: str | None = Field(
        None,
        description="The data class defining the sensitivity level for this field, "
        "according to the organization's classification scheme.",
        json_schema_extra={"example": "restricted"},
    )
    tags: list[str] | None = Field(
        None,
        description="Custom metadata to provide additional context.",
        json_schema_extra={"example": ["orders", "checkout"]},
    )
    links: dict[str, str] | None = Field(
        None,
        description="Additional external documentation links.",
        json_schema_extra={
            "example": {"wikipedia": "https://en.wikipedia.org/wiki/Stock_keeping_unit"}
        },
    )
    ref: str | None = Field(
        None,
        alias="$ref",
        description="A reference URI to a definition in the specification, internally or externally.",
        json_schema_extra={"example": "#/definitions/order_id"},
    )
    fields: dict[str, "FieldObject"] | None = Field(
        None,
        description="The nested fields of the object, record, or struct. "
        "Use only when type is object, record, or struct.",
        json_schema_extra={
            "example": {
                "street": {"type": "string", "description": "Street name"},
                "number": {"type": "integer", "description": "House number"},
            }
        },
    )
    items: Optional["FieldObject"] = Field(
        None,
        description="The type of the elements in the array. Use only when type is array.",
        json_schema_extra={"example": {"type": "string", "description": "Product SKU"}},
    )
    keys: Optional["FieldObject"] = Field(
        None,
        description="Describes the key structure of a map. Use only when type is map.",
        json_schema_extra={"example": {"type": "string", "description": "Country code"}},
    )
    values: Optional["FieldObject"] = Field(
        None,
        description="Describes the value structure of a map. Use only when type is map.",
        json_schema_extra={"example": {"type": "string", "description": "Country name"}},
    )
    config: ConfigObject | None = Field(
        None,
        description="Any additional key-value pairs that might be useful for further tooling.",
        json_schema_extra={
            "example": {
                "jsonType": "string",
                "jsonFormat": "date-time",
            }
        },
    )


FieldObject.model_rebuild()
