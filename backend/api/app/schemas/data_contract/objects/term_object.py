from typing import Optional

from pydantic import Field

from ....utils.example_model import BaseModelWithExample


class TermObject(BaseModelWithExample):
    """
    Represents the terms and conditions of a data contract.

    This class defines the structure for the 'terms' section of a data contract,
    including details such as usage terms, limitations, billing information, and notice period.
    """

    usage: Optional[str] = Field(
        None,
        description="The way the data is expected to be used. Can contain business and technical information.",
        example="Data can be used for reports, analytics and machine learning use cases.",
    )
    limitations: Optional[str] = Field(
        None,
        description="Restrictions on how the data can be used, including technical limitations or usage restrictions.",
        example="Not suitable for real-time use cases. Data may not be used to identify individual customers.",
    )
    billing: Optional[str] = Field(
        None,
        description="The pricing model for using the data (e.g., free, monthly fee, or metered pay-per-use).",
        example="5000 USD per month",
    )
    notice_period: Optional[str] = Field(
        None,
        description="Period of time required to terminate or modify the data usage agreement. Uses ISO-8601 format.",
        example="P3M",
    )
