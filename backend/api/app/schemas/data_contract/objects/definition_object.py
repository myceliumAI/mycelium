from typing import Any, Dict, List, Optional

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
        example="order_id",
    )
    type: DataType = Field(..., description="REQUIRED. The logical data type.", example="text")
    domain: Optional[str] = Field(
        "global",
        description="The domain in which this definition is valid. Default: global.",
        example="checkout",
    )
    title: Optional[str] = Field(
        None,
        description="The business name of this definition.",
        example="Order ID",
    )
    description: Optional[str] = Field(
        None,
        description="Clear and concise explanations related to the domain.",
        example="An internal ID that identifies an order in the online shop.",
    )
    enum: Optional[List[str]] = Field(
        None,
        description="A value must be equal to one of the elements in this array value. "
        "Only evaluated if the value is not null.",
        example=["PENDING", "PROCESSING", "SHIPPED", "DELIVERED"],
    )
    format: Optional[str] = Field(
        None,
        description="Specifies the format of the field (e.g., email, uri, uuid).",
        example="uuid",
    )
    precision: Optional[int] = Field(
        38,
        description="The maximum number of digits in a number. Only applies to numeric values.",
        example=10,
    )
    scale: Optional[int] = Field(
        0,
        description="The maximum number of decimal places in a number. Only applies to numeric values.",
        example=2,
    )
    min_length: Optional[int] = Field(
        None,
        description="A value must be greater than, or equal to, the value of this. "
        "Only applies to unicode character sequences types.",
        example=10,
    )
    max_length: Optional[int] = Field(
        None,
        description="A value must be less than, or equal to, the value of this. "
        "Only applies to unicode character sequences types.",
        example=20,
    )
    pattern: Optional[str] = Field(
        None,
        description="A value must be valid according to the ECMA-262 regular expression dialect. "
        "Only applies to unicode character sequences types.",
        example="^[A-Za-z0-9]{8,14}$",
    )
    minimum: Optional[float] = Field(
        None,
        description="A value of a number must be greater than, or equal to, the value of this. "
        "Only applies to numeric values.",
        example=0,
    )
    exclusive_minimum: Optional[float] = Field(
        None,
        description="A value of a number must be greater than the value of this. " "Only applies to numeric values.",
        example=0,
    )
    maximum: Optional[float] = Field(
        None,
        description="A value of a number must be less than, or equal to, the value of this. "
        "Only applies to numeric values.",
        example=1000000,
    )
    exclusive_maximum: Optional[float] = Field(
        None,
        description="A value of a number must be less than the value of this. " "Only applies to numeric values.",
        example=1000000,
    )
    example: Optional[Any] = Field(
        None,
        description="An example value.",
        example="243c25e5-a081-43a9-aeab-6d5d5b6cb5e2",
    )
    pii: Optional[bool] = Field(
        None,
        description="An indication, if this field contains Personal Identifiable Information (PII).",
        example=True,
    )
    classification: Optional[str] = Field(
        None,
        description="The data class defining the sensitivity level for this field, "
        "according to the organization's classification scheme.",
        example="restricted",
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Custom metadata to provide additional context.",
        example=["orders", "checkout"],
    )
    links: Optional[Dict[str, HttpUrl]] = Field(
        None,
        description="Additional external documentation links.",
        example={"documentation": "https://docs.example.com/order-id"},
    )
    fields: Optional[Dict[str, FieldObject]] = Field(
        None,
        description="The nested fields of the object, record, or struct. "
        "Use only when type is object, record, or struct.",
        example={
            "street": FieldObject(type="string", description="Street name"),
            "number": FieldObject(type="integer", description="House number"),
        },
    )
    items: Optional[FieldObject] = Field(
        None,
        description="The type of the elements in the array. Use only when type is array.",
        example=FieldObject(type="string", description="Product SKU"),
    )
    keys: Optional[FieldObject] = Field(
        None,
        description="Describes the key structure of a map. Use only when type is map.",
        example=FieldObject(type="string", description="Country code"),
    )
    values: Optional[FieldObject] = Field(
        None,
        description="Describes the value structure of a map. Use only when type is map.",
        example=FieldObject(type="string", description="Country name"),
    )

    model_config = ConfigDict(extra="allow")
