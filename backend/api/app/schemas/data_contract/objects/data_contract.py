from typing import Dict, List, Optional

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
        example="11.9.3",
    )
    id: str = Field(
        ...,
        description="REQUIRED. An organization-wide unique technical identifier.",
        example="urn:datacontract:checkout:orders-latest",
    )
    info: InfoObject = Field(
        ...,
        description="REQUIRED. Specifies the metadata of the data contract.",
        example=InfoObject.get_example(),
    )
    servers: Optional[Dict[str, ServerObject]] = Field(
        None,
        description="Specifies the servers of the data contract.",
        example={"production": ServerObject.get_example()},
    )
    terms: Optional[TermObject] = Field(
        None,
        description="Specifies the terms and conditions of the data contract.",
        example=TermObject.get_example(),
    )
    models: Optional[Dict[str, ModelObject]] = Field(
        None,
        description="Specifies the logical data model.",
        example={"orders": ModelObject.get_example()},
    )
    definitions: Optional[Dict[str, DefinitionObject]] = Field(
        None,
        description="Specifies definitions.",
        example={"order_id": DefinitionObject.get_example()},
    )
    examples: Optional[List[ExampleObject]] = Field(
        None,
        description="Specifies example data sets for the data model.",
        example=[ExampleObject.get_example()],
    )
    service_level: Optional[ServiceLevelObject] = Field(
        None,
        description="Specifies the service level of the provided data.",
        example=ServiceLevelObject.get_example(),
    )
    quality: Optional[QualityObject] = Field(
        None,
        description="Specifies the quality attributes and checks.",
        example=QualityObject.get_example(),
    )
    links: Optional[Dict[str, HttpUrl]] = Field(
        None,
        description="Additional external documentation links.",
        example={"datacontractCli": "https://cli.datacontract.com"},
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Custom metadata to provide additional context.",
        example=["checkout", "orders", "s3"],
    )

    model_config = ConfigDict(populate_by_name=True)
