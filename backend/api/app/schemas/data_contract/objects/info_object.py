from typing import Literal

from pydantic import Field

from ....utils.example_model import BaseModelWithExample
from .contact_object import ContactObject


class InfoObject(BaseModelWithExample):
    """
    Represents the metadata information of a data contract.

    This class defines the structure for the 'info' section of a data contract,
    including details such as title, version, status, description, owner, and contact information.
    """

    title: str = Field(
        ...,
        description="REQUIRED. The title of the data contract.",
        json_schema_extra={"example": "Customer Orders Data Contract"},
    )
    version: str = Field(
        ...,
        description="REQUIRED. The version of the data contract document (which is distinct from the Data Contract Specification version or the Data Product implementation version).",
        json_schema_extra={"example": "1.0.0"},
    )
    status: Literal["proposed", "in development", "active", "deprecated", "retired"] | None = Field(
        None,
        description="The status of the data contract.",
        json_schema_extra={"example": "active"},
    )
    description: str | None = Field(
        None,
        description="A description of the data contract.",
        json_schema_extra={
            "example": "This data contract defines the structure and rules for customer order data."
        },
    )
    owner: str | None = Field(
        None,
        description="The owner or team responsible for managing the data contract and providing the data.",
        json_schema_extra={"example": "Customer Data Team"},
    )
    contact: ContactObject | None = Field(
        None,
        json_schema_extra={"example": ContactObject.get_example()},
        description="Contact information for the data contract.",
    )
