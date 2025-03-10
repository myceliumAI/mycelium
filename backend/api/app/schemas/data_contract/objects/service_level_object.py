from pydantic import Field

from ....utils.example_model import BaseModelWithExample


class AvailabilityObject(BaseModelWithExample):
    """
    Represents the availability service level for a data contract.

    This class defines the structure for the 'availability' section of service levels,
    including a description and the guaranteed uptime percentage.
    """

    description: str | None = Field(
        None,
        description="A description of the availability service level.",
        json_schema_extra={"example": "The server is available during support hours"},
    )
    percentage: str | None = Field(
        None,
        description="The guaranteed uptime in percent (e.g., '99.9%').",
        json_schema_extra={"example": "99.9%"},
    )


class RetentionObject(BaseModelWithExample):
    """
    Represents the retention service level for a data contract.

    This class defines the structure for the 'retention' section of service levels,
    including details about how long data will be available.
    """

    description: str | None = Field(
        None,
        description="A description of the retention service level.",
        json_schema_extra={"example": "Data is retained for one year"},
    )
    period: str | None = Field(
        None,
        description="The period of time data is available (e.g., '1 year', 'P1Y').",
        json_schema_extra={"example": "P1Y"},
    )
    unlimited: bool | None = Field(
        None,
        description="Indicator that data is kept forever.",
        json_schema_extra={"example": False},
    )
    timestamp_field: str | None = Field(
        None,
        description="Reference to the field containing the relevant timestamp.",
        json_schema_extra={"example": "orders.order_timestamp"},
    )


class LatencyObject(BaseModelWithExample):
    """
    Represents the latency service level for a data contract.

    This class defines the structure for the 'latency' section of service levels,
    including details about the maximum time from source to destination.
    """

    description: str | None = Field(
        None,
        description="A description of the latency service level.",
        json_schema_extra={
            "example": "Data is available within 25 hours after the order was placed"
        },
    )
    threshold: str | None = Field(
        None,
        description="Maximum duration between source and processed timestamps.",
        json_schema_extra={"example": "25h"},
    )
    source_timestamp_field: str | None = Field(
        None,
        description="Reference to the field with the source timestamp.",
        json_schema_extra={"example": "orders.order_timestamp"},
    )
    processed_timestamp_field: str | None = Field(
        None,
        description="Reference to the field with the processing timestamp.",
        json_schema_extra={"example": "orders.processed_timestamp"},
    )


class FreshnessObject(BaseModelWithExample):
    """
    Represents the freshness service level for a data contract.

    This class defines the structure for the 'freshness' section of service levels,
    including details about the maximum age of the youngest entry.
    """

    description: str | None = Field(
        None,
        description="A description of the freshness service level.",
        json_schema_extra={"example": "The age of the youngest row in a table."},
    )
    threshold: str | None = Field(
        None,
        description="Maximum age of the youngest entry.",
        json_schema_extra={"example": "25h"},
    )
    timestamp_field: str | None = Field(
        None,
        description="Reference to the field containing the relevant timestamp.",
        json_schema_extra={"example": "orders.order_timestamp"},
    )


class FrequencyObject(BaseModelWithExample):
    """
    Represents the frequency service level for a data contract.

    This class defines the structure for the 'frequency' section of service levels,
    including details about how often data is updated.
    """

    description: str | None = Field(
        None,
        description="A description of the frequency service level.",
        json_schema_extra={"example": "Data is delivered once a day"},
    )
    type: str | None = Field(
        None,
        description="Type of data processing (e.g., 'batch', 'streaming').",
        json_schema_extra={"example": "batch"},
    )
    interval: str | None = Field(
        None,
        description="How often the pipeline is triggered (for batch processing).",
        json_schema_extra={"example": "daily"},
    )
    cron: str | None = Field(
        None,
        description="Cron expression for when the pipeline is triggered.",
        json_schema_extra={"example": "0 0 * * *"},
    )


class SupportObject(BaseModelWithExample):
    """
    Represents the support service level for a data contract.

    This class defines the structure for the 'support' section of service levels,
    including details about support availability and response times.
    """

    description: str | None = Field(
        None,
        description="A description of the support service level.",
        json_schema_extra={
            "example": "The data is available during typical business hours at headquarters"
        },
    )
    time: str | None = Field(
        None,
        description="Times when support is available (e.g., '24/7', 'business hours').",
        json_schema_extra={"example": "9am to 5pm in EST on business days"},
    )
    response_time: str | None = Field(
        None,
        description="Expected time for support to acknowledge a request.",
        json_schema_extra={"example": "1h"},
    )


class BackupObject(BaseModelWithExample):
    """
    Represents the backup service level for a data contract.

    This class defines the structure for the 'backup' section of service levels,
    including details about data backup procedures and recovery objectives.
    """

    description: str | None = Field(
        None,
        description="A description of the backup service level.",
        json_schema_extra={"example": "Data is backed up once a week, every Sunday at 0:00 UTC."},
    )
    interval: str | None = Field(
        None,
        description="How often data will be backed up.",
        json_schema_extra={"example": "weekly"},
    )
    cron: str | None = Field(
        None,
        description="Cron expression for when data will be backed up.",
        json_schema_extra={"example": "0 0 * * 0"},
    )
    recovery_time: str | None = Field(
        None,
        description="Maximum time allowed to restore data from a backup.",
        json_schema_extra={"example": "24 hours"},
    )
    recovery_point: str | None = Field(
        None,
        description="Maximum acceptable age of files for recovery.",
        json_schema_extra={"example": "1 week"},
    )


class ServiceLevelObject(BaseModelWithExample):
    """
    Represents the service levels for a data contract.

    This class defines various service level attributes such as availability,
    retention, latency, freshness, frequency of data delivery, support, and backup.
    """

    availability: AvailabilityObject | None = Field(
        None,
        description="Availability service level.",
        json_schema_extra={"example": AvailabilityObject.get_example()},
    )
    retention: RetentionObject | None = Field(
        None,
        description="Data retention service level.",
        json_schema_extra={"example": RetentionObject.get_example()},
    )
    latency: LatencyObject | None = Field(
        None,
        description="Latency service level.",
        json_schema_extra={"example": LatencyObject.get_example()},
    )
    freshness: FreshnessObject | None = Field(
        None,
        description="Data freshness service level.",
        json_schema_extra={"example": FreshnessObject.get_example()},
    )
    frequency: FrequencyObject | None = Field(
        None,
        description="Data delivery frequency service level.",
        json_schema_extra={"example": FrequencyObject.get_example()},
    )
    support: SupportObject | None = Field(
        None,
        description="Support service level.",
        json_schema_extra={"example": SupportObject.get_example()},
    )
    backup: BackupObject | None = Field(
        None,
        description="Backup service level.",
        json_schema_extra={"example": BackupObject.get_example()},
    )
