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
    description: str | None = Field(
        None,
        description="An optional string describing the server.",
        example="One folder per model. One file per day.",
    )
    environment: str | None = Field(
        None,
        description="An optional string describing the environment, e.g., prod, sit, stg.",
        example="prod",
    )

    # Fields for S3 Server Object
    location: str | None = Field(
        None,
        description="S3 URL, starting with s3://",
        example="s3://datacontract-example-orders-latest/data/{model}/*.json",
    )
    endpoint_url: str | None = Field(
        None,
        description="The server endpoint for S3-compatible servers",
        example="https://s3.amazonaws.com",
    )
    format: str | None = Field(
        None,
        description="Format of files, such as parquet, delta, json, csv",
        example="json",
    )
    delimiter: str | None = Field(
        None,
        description="(Only for format = json) How multiple json documents are delimited within one file",
        example="new_line",
    )

    # Fields for BigQuery Server Object
    project: str | None = Field(
        None,
        description="The GCP project name.",
        example="my-gcp-project",
    )
    dataset: str | None = Field(
        None,
        description="The BigQuery dataset.",
        example="orders_dataset",
    )

    # Fields for Redshift Server Object
    account: str | None = Field(
        None,
        description="The Redshift account.",
        example="my-redshift-account",
    )
    database: str | None = Field(
        None,
        description="The database name.",
        example="orders_db",
    )
    schema_name: str | None = Field(
        None,
        description="The schema name.",
        example="public",
    )
    cluster_identifier: str | None = Field(
        None,
        description="Identifier of the Redshift cluster.",
        example="my-redshift-cluster",
    )
    host: str | None = Field(
        None,
        description="Host of the Redshift cluster.",
        example="my-redshift-cluster.abcdefg.us-west-2.redshift.amazonaws.com",
    )
    port: int | None = Field(
        None,
        description="Port of the Redshift cluster.",
        example=5439,
    )
    endpoint: str | None = Field(
        None,
        description="Endpoint of the Redshift cluster.",
        example="my-redshift-cluster.abcdefg.us-west-2.redshift.amazonaws.com:5439",
    )

    # Fields for Azure Server Object
    # Note: 'location' field is reused from S3 Server Object

    # Fields for SQL-Server Server Object
    driver: str | None = Field(
        None,
        description="The name of the supported driver.",
        example="ODBC Driver 17 for SQL Server",
    )

    # Fields for Snowflake Server Object
    # Note: 'account', 'database', and 'schema' fields are reused from Redshift Server Object

    # Fields for Databricks Server Object
    catalog: str | None = Field(
        None,
        description="The name of the Hive or Unity catalog.",
        example="my_catalog",
    )

    # Fields for Postgres Server Object
    # Note: 'host', 'port', 'database', and 'schema' fields are reused from previous objects

    # Fields for Oracle Server Object
    service_name: str | None = Field(
        None,
        description="The name of the Oracle service.",
        example="ORCL",
    )

    # Fields for Kafka Server Object
    topic: str | None = Field(
        None,
        description="The Kafka topic name.",
        example="orders_topic",
    )

    # Fields for Pub/Sub Server Object
    # Note: 'project' and 'topic' fields are reused from previous objects

    # Fields for sftp Server Object
    # Note: 'location', 'format', and 'delimiter' fields are reused from S3 Server Object

    # Fields for AWS Kinesis Data Streams Server Object
    stream: str | None = Field(
        None,
        description="The name of the Kinesis data stream.",
        example="orders_stream",
    )
    region: str | None = Field(
        None,
        description="AWS region, e.g., eu-west-1.",
        example="eu-west-1",
    )

    # Fields for Trino Server Object
    # Note: 'host', 'port', 'catalog', and 'schema' fields are reused from previous objects

    # Fields for Local Server Object
    path: str | None = Field(
        None,
        description="The relative or absolute path to the data file(s).",
        example="/data/orders/*.json",
    )
