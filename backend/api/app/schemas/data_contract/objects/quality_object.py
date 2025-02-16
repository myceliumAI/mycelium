from typing import Literal

from pydantic import Field

from ....utils.example_model import BaseModelWithExample


class SodaCLQualityObject(BaseModelWithExample):
    """
    Represents quality attributes in Soda Checks Language.
    """

    type: Literal["SodaCL"] = Field(
        "SodaCL",
        description="The type of the schema, always 'SodaCL'.",
        json_schema_extra={"example": "SodaCL"},
    )
    specification: str = Field(
        ...,
        description="The SodaCL specification as a string or inline YAML.",
        json_schema_extra={
            "example": """
            checks for orders:
              - row_count > 0
              - duplicate_count(order_id) = 0
            checks for line_items:
              - row_count > 0
            """
        },
    )


class MonteCarloQualityObject(BaseModelWithExample):
    """
    Represents quality attributes defined as Monte Carlo's Monitors as Code.
    """

    type: Literal["montecarlo"] = Field(
        "montecarlo",
        description="The type of the schema, always 'montecarlo'.",
        json_schema_extra={"example": "montecarlo"},
    )
    specification: str = Field(
        ...,
        description="The Monte Carlo specification as a string or inline YAML.",
        json_schema_extra={
            "example": """
            montecarlo:
              field_health:
                - table: project:dataset.table_name
              timestamp_field: created
          dimension_tracking:
            - table: project:dataset.table_name
                timestamp_field: created
                field: order_status
            """
        },
    )


class GreatExpectationsQualityObject(BaseModelWithExample):
    """
    Represents quality attributes defined as Great Expectations Expectations.
    """

    type: Literal["great-expectations"] = Field(
        "great-expectations",
        description="The type of the schema, always 'great-expectations'.",
        json_schema_extra={"example": "great-expectations"},
    )
    specification: dict = Field(
        ...,
        description="The Great Expectations specification as a dictionary.",
        json_schema_extra={
            "example": {
                "orders": """
                [
                        {
                        "expectation_type": "expect_table_row_count_to_be_between",
                        "kwargs": {
                            "min_value": 10
                        },
                        "meta": {}
                    }
                ]
            """
            }
        },
    )


class CustomQualityObject(BaseModelWithExample):
    """
    Represents custom quality attributes.
    """

    type: Literal["custom"] = Field(
        "custom",
        description="The type of the schema, always 'custom'.",
        json_schema_extra={"example": "custom"},
    )
    specification: str = Field(
        ...,
        description="The custom specification as a string.",
        json_schema_extra={"example": "Custom quality specification goes here."},
    )


class QualityObject(BaseModelWithExample):
    """
    Represents the quality object containing quality attributes and checks.

    :param str type: REQUIRED. The type of the schema (e.g., 'SodaCL', 'montecarlo', 'great-expectations', 'custom').
    :param Union[SodaCLQualityObject, MonteCarloQualityObject, GreatExpectationsQualityObject, CustomQualityObject] specification: REQUIRED. The specification of the quality attributes.
    """

    type: str = Field(
        ...,
        description="REQUIRED. The type of the schema.",
        json_schema_extra={"example": "SodaCL"},
    )
    specification: (
        SodaCLQualityObject
        | MonteCarloQualityObject
        | GreatExpectationsQualityObject
        | CustomQualityObject
    ) = Field(
        ...,
        description="REQUIRED. The specification of the quality attributes.",
        json_schema_extra={"example": SodaCLQualityObject.get_example()},
    )
