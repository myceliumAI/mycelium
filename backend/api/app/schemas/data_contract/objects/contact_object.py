from typing import Optional

from pydantic import EmailStr, Field, HttpUrl

from ....utils.example_model import BaseModelWithExample


class ContactObject(BaseModelWithExample):
    """
    Represents contact information for the data contract.

    This class defines the structure for the 'contact' section of a data contract,
    including details such as name, URL, and email of the contact person/organization.
    """

    name: Optional[str] = Field(
        None,
        description="The identifying name of the contact person/organization.",
        example="John Doe",
    )
    url: Optional[HttpUrl] = Field(
        None,
        description="The URL pointing to the contact information. This MUST be in the form of a URL.",
        example="https://example.com/contact",
    )
    email: Optional[EmailStr] = Field(
        None,
        description="The email address of the contact person/organization. This MUST be in the form of an email address.",
        example="john.doe@example.com",
    )
