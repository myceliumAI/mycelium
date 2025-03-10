from pydantic import AliasChoices, ConfigDict, Field, HttpUrl

from ....utils.example_model import BaseModelWithExample
from .definition_object import DefinitionObject
from .example_object import ExampleObject
from .info_object import InfoObject
from .model_object import ModelObject
from .quality_object import QualityObject
from .server_object import ServerObject
from .service_level_object import ServiceLevelObject
from .term_object import TermObject


class DataContract(BaseModelWithExample):
    """
    Represents a Data Contract following the specifications from datacontract.com.
    """

    data_contract_specification: str = Field(
        ...,
        description="REQUIRED. Specifies the Data Contract Specification being used.",
        validation_alias=AliasChoices("data_contract_specification", "dataContractSpecification"),
        json_schema_extra={"example": "11.9.3"},
    )
    id: str = Field(
        ...,
        description="REQUIRED. An organization-wide unique technical identifier.",
        json_schema_extra={"example": "urn:datacontract:checkout:orders-latest"},
    )
    info: InfoObject = Field(
        ...,
        description="REQUIRED. Specifies the metadata of the data contract.",
        json_schema_extra={"example": InfoObject.get_example()},
    )
    servers: dict[str, ServerObject] | None = Field(
        None,
        description="Specifies the servers of the data contract.",
        json_schema_extra={"example": {"production": ServerObject.get_example()}},
    )
    terms: TermObject | None = Field(
        None,
        description="Specifies the terms and conditions of the data contract.",
        json_schema_extra={"example": TermObject.get_example()},
    )
    models: dict[str, ModelObject] | None = Field(
        None,
        description="Specifies the logical data model.",
        json_schema_extra={"example": {"orders": ModelObject.get_example()}},
    )
    definitions: dict[str, DefinitionObject] | None = Field(
        None,
        description="Specifies definitions.",
        json_schema_extra={"example": {"order_id": DefinitionObject.get_example()}},
    )
    examples: list[ExampleObject] | None = Field(
        None,
        description="Specifies example data sets for the data model.",
        json_schema_extra={"example": [ExampleObject.get_example()]},
    )
    service_level: ServiceLevelObject | None = Field(
        None,
        description="Specifies the service level of the provided data.",
        json_schema_extra={"example": ServiceLevelObject.get_example()},
    )
    quality: QualityObject | None = Field(
        None,
        description="Specifies the quality attributes and checks.",
        json_schema_extra={"example": QualityObject.get_example()},
    )
    links: dict[str, HttpUrl] | None = Field(
        None,
        description="Additional external documentation links.",
        json_schema_extra={"example": {"datacontractCli": "https://cli.datacontract.com"}},
    )
    tags: list[str] | None = Field(
        None,
        description="Custom metadata to provide additional context.",
        json_schema_extra={"example": ["checkout", "orders", "s3"]},
    )

    model_config = ConfigDict(populate_by_name=True)
