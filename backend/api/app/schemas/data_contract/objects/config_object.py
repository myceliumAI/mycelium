from typing import Any

from pydantic import ConfigDict, Field

from ....utils.example_model import BaseModelWithExample


class ConfigObject(BaseModelWithExample):
    """
    Represents additional metadata for models and fields in a data contract.

    This class defines the structure for the 'config' section, which can be used
    to specify various properties that may be utilized by tools for tasks such as
    code generation, physical data type specification, and test toggling.
    """

    avro_namespace: str | None = Field(
        None,
        description="(Only on model level) The namespace to use when importing and exporting the data model from / to Apache Avro.",
        json_schema_extra={"example": "my.namespace"},
    )
    avro_type: str | None = Field(
        None,
        description="(Only on field level) Specify the field type to use when exporting the data model to Apache Avro.",
        json_schema_extra={"example": "long"},
    )
    avro_logical_type: str | None = Field(
        None,
        description="(Only on field level) Specify the logical field type to use when exporting the data model to Apache Avro.",
        json_schema_extra={"example": "timestamp-millis"},
    )
    bigquery_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a BigQuery table.",
        json_schema_extra={"example": "NUMERIC(5, 2)"},
    )
    snowflake_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Snowflake table.",
        json_schema_extra={"example": "TIMESTAMP_LTZ"},
    )
    redshift_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Redshift table.",
        json_schema_extra={"example": "SMALLINT"},
    )
    sqlserver_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a SQL Server table.",
        json_schema_extra={"example": "DATETIME2"},
    )
    databricks_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in a Databricks table.",
        json_schema_extra={"example": "TIMESTAMP"},
    )
    glue_type: str | None = Field(
        None,
        description="(Only on field level) Specify the physical column type that is used in an AWS Glue Data Catalog table.",
        json_schema_extra={"example": "timestamp"},
    )

    model_config = ConfigDict(extra="allow")

    def __init__(self, **data: Any):
        """
        Initialize the ConfigObject with any additional fields as Specification Extensions.

        :param Dict[str, Any] data: Key-value pairs for configuration, including standard fields and extensions.
        """
        super().__init__(**data)
        for key, value in data.items():
            if not hasattr(self, key):
                setattr(self, key, value)
