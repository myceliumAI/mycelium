from typing import Optional

from pydantic import Field

from ....utils.example_model import BaseModelWithExample


class ServerObject(BaseModelWithExample):
    """
    Represents a server object in a data contract.

    This class defines the structure and properties of a server,
    including its type, description, environment, and other type-specific fields.
    """

    type: str = Field(
        ...,
        description="REQUIRED. The type of the data product technology that implements the data contract.",
        example="s3",
    )
    description: Optional[str] = Field(
        None,
        description="An optional string describing the server.",
        example="One folder per model. One file per day.",
    )
    environment: Optional[str] = Field(
        None,
        description="An optional string describing the environment, e.g., prod, sit, stg.",
        example="prod",
    )

    # Fields for S3 Server Object
    location: Optional[str] = Field(
        None,
        description="S3 URL, starting with s3://",
        example="s3://datacontract-example-orders-latest/data/{model}/*.json",
    )
    endpoint_url: Optional[str] = Field(
        None,
        description="The server endpoint for S3-compatible servers",
        example="https://s3.amazonaws.com",
    )
    format: Optional[str] = Field(
        None,
        description="Format of files, such as parquet, delta, json, csv",
        example="json",
    )
    delimiter: Optional[str] = Field(
        None,
        description="(Only for format = json) How multiple json documents are delimited within one file",
        example="new_line",
    )

    # Fields for BigQuery Server Object
    project: Optional[str] = Field(
        None,
        description="The GCP project name.",
        example="my-gcp-project",
    )
    dataset: Optional[str] = Field(
        None,
        description="The BigQuery dataset.",
        example="orders_dataset",
    )

    # Fields for Redshift Server Object
    account: Optional[str] = Field(
        None,
        description="The Redshift account.",
        example="my-redshift-account",
    )
    database: Optional[str] = Field(
        None,
        description="The database name.",
        example="orders_db",
    )
    schema_name: Optional[str] = Field(
        None,
        description="The schema name.",
        example="public",
    )
    cluster_identifier: Optional[str] = Field(
        None,
        description="Identifier of the Redshift cluster.",
        example="my-redshift-cluster",
    )
    host: Optional[str] = Field(
        None,
        description="Host of the Redshift cluster.",
        example="my-redshift-cluster.abcdefg.us-west-2.redshift.amazonaws.com",
    )
    port: Optional[int] = Field(
        None,
        description="Port of the Redshift cluster.",
        example=5439,
    )
    endpoint: Optional[str] = Field(
        None,
        description="Endpoint of the Redshift cluster.",
        example="my-redshift-cluster.abcdefg.us-west-2.redshift.amazonaws.com:5439",
    )

    # Fields for Azure Server Object
    # Note: 'location' field is reused from S3 Server Object

    # Fields for SQL-Server Server Object
    driver: Optional[str] = Field(
        None,
        description="The name of the supported driver.",
        example="ODBC Driver 17 for SQL Server",
    )

    # Fields for Snowflake Server Object
    # Note: 'account', 'database', and 'schema' fields are reused from Redshift Server Object

    # Fields for Databricks Server Object
    catalog: Optional[str] = Field(
        None,
        description="The name of the Hive or Unity catalog.",
        example="my_catalog",
    )

    # Fields for Postgres Server Object
    # Note: 'host', 'port', 'database', and 'schema' fields are reused from previous objects

    # Fields for Oracle Server Object
    service_name: Optional[str] = Field(
        None,
        description="The name of the Oracle service.",
        example="ORCL",
    )

    # Fields for Kafka Server Object
    topic: Optional[str] = Field(
        None,
        description="The Kafka topic name.",
        example="orders_topic",
    )

    # Fields for Pub/Sub Server Object
    # Note: 'project' and 'topic' fields are reused from previous objects

    # Fields for sftp Server Object
    # Note: 'location', 'format', and 'delimiter' fields are reused from S3 Server Object

    # Fields for AWS Kinesis Data Streams Server Object
    stream: Optional[str] = Field(
        None,
        description="The name of the Kinesis data stream.",
        example="orders_stream",
    )
    region: Optional[str] = Field(
        None,
        description="AWS region, e.g., eu-west-1.",
        example="eu-west-1",
    )

    # Fields for Trino Server Object
    # Note: 'host', 'port', 'catalog', and 'schema' fields are reused from previous objects

    # Fields for Local Server Object
    path: Optional[str] = Field(
        None,
        description="The relative or absolute path to the data file(s).",
        example="/data/orders/*.json",
    )
