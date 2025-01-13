from typing import Any, Dict

from ..models.data_contract import DataContract as DBDataContract
from ..schemas.data_contract.objects.data_contract import (
    DataContract as PydanticDataContract,
)


def pydantic_to_db_model(pydantic_model: PydanticDataContract) -> DBDataContract:
    """
    Converts a Pydantic DataContract model to a SQLAlchemy DataContract model.

    :param PydanticDataContract pydantic_model: The Pydantic model to convert.
    :return DBDataContract: The corresponding SQLAlchemy model.
    """
    db_model = DBDataContract(
        id=pydantic_model.id,
        data_contract_specification=pydantic_model.data_contract_specification,
        info=pydantic_model.info.model_dump(mode="json"),
        servers=(
            {k: v.model_dump(mode="json") for k, v in pydantic_model.servers.items()}
            if pydantic_model.servers
            else None
        ),
        terms=pydantic_model.terms.model_dump(mode="json") if pydantic_model.terms else None,
        models=(
            {k: v.model_dump(mode="json") for k, v in pydantic_model.models.items()} if pydantic_model.models else None
        ),
        definitions=(
            {k: v.model_dump(mode="json") for k, v in pydantic_model.definitions.items()}
            if pydantic_model.definitions
            else None
        ),
        examples=(
            [example.model_dump(mode="json") for example in pydantic_model.examples]
            if pydantic_model.examples
            else None
        ),
        service_level=(pydantic_model.service_level.model_dump(mode="json") if pydantic_model.service_level else None),
        quality=pydantic_model.quality.model_dump(mode="json") if pydantic_model.quality else None,
        links={str(k): str(v) for k, v in pydantic_model.links.items()} if pydantic_model.links else None,
        tags=pydantic_model.tags,
    )
    return db_model


def db_to_pydantic_model(db_model: DBDataContract) -> PydanticDataContract:
    """
    Converts a SQLAlchemy DataContract model to a Pydantic DataContract model.

    :param DBDataContract db_model: The SQLAlchemy model to convert.
    :return PydanticDataContract: The corresponding Pydantic model.
    """
    db_dict: Dict[str, Any] = {c.name: getattr(db_model, c.name) for c in db_model.__table__.columns}

    # Convert servers back to a dictionary if it exists
    if db_dict.get("servers"):
        db_dict["servers"] = {k: v for k, v in db_dict["servers"].items()}

    # Use Pydantic's model_validate to create the Pydantic model
    return PydanticDataContract.model_validate(db_dict)
