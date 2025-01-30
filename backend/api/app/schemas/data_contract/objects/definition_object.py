from typing import Any

from pydantic import ConfigDict, Field, HttpUrl

from ....utils.example_model import BaseModelWithExample
from .data_type import DataType
from .field_object import FieldObject


class DefinitionObject(BaseModelWithExample):
    """
    Represents a definition object in a data contract.

    This class defines the structure and properties of a definition,
    including its name, type, domain, and various other attributes.
    It also allows for additional arbitrary key-value pairs.
    """

    name: str = Field(
        ...,
        description="REQUIRED. The technical name of this definition.",
        json_schema_extra={"example": "order_id"},
    )
    type: DataType = Field(
        ...,
        description="REQUIRED. The logical data type.",
        json_schema_extra={"example": "text"},
    )
    domain: str | None = Field(
        "global",
        description="The domain in which this definition is valid. Default: global.",
        json_schema_extra={"example": "checkout"},
    )
    title: str | None = Field(
        None,
        description="The business name of this definition.",
        json_schema_extra={"example": "Order ID"},
    )
    description: str | None = Field(
        None,
        description="Clear and concise explanations related to the domain.",
        json_schema_extra={
            "example": "An internal ID that identifies an order in the online shop."
        },
    )
    enum: list[str] | None = Field(
        None,
        description="A value must be equal to one of the elements in this array value. "
        "Only evaluated if the value is not null.",
        json_schema_extra={"example": ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED"]},
    )
    format: str | None = Field(
        None,
        description="Specifies the format of the field (e.g., email, uri, uuid).",
        json_schema_extra={"example": "uuid"},
    )
    precision: int | None = Field(
        38,
        description="The maximum number of digits in a number. Only applies to numeric values.",
        json_schema_extra={"example": 10},
    )
    scale: int | None = Field(
        0,
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
    links: dict[str, HttpUrl] | None = Field(
        None,
        description="Additional external documentation links.",
        json_schema_extra={"example": {"documentation": "https://docs.example.com/order-id"}},
    )
    fields: dict[str, FieldObject] | None = Field(
        None,
        description="The nested fields of the object, record, or struct. "
        "Use only when type is object, record, or struct.",
        json_schema_extra={
            "example": {
                "street": FieldObject(type="string", description="Street name"),
                "number": FieldObject(type="integer", description="House number"),
            }
        },
    )
    items: FieldObject | None = Field(
        None,
        description="The type of the elements in the array. Use only when type is array.",
        json_schema_extra={"example": FieldObject(type="string", description="Product SKU")},
    )
    keys: FieldObject | None = Field(
        None,
        description="Describes the key structure of a map. Use only when type is map.",
        json_schema_extra={"example": FieldObject(type="string", description="Country code")},
    )
    values: FieldObject | None = Field(
        None,
        description="Describes the value structure of a map. Use only when type is map.",
        json_schema_extra={"example": FieldObject(type="string", description="Country name")},
    )

    model_config = ConfigDict(extra="allow")
