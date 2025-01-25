import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.data_contract import DataContract as DataContractModel
from ..schemas.data_contract.objects.data_contract import DataContract
from ..schemas.data_contract.routes.data_contract_create import DataContractCreate
from ..schemas.data_contract.routes.data_contract_delete import DataContractDelete
from ..schemas.data_contract.routes.data_contract_update import DataContractUpdate
from ..utils.config import settings
from ..utils.tools import db_to_pydantic_model, pydantic_to_db_model


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def create_data_contract(db: Session, data_contract: DataContractCreate) -> DataContract:
    """
    Creates a new data contract in the database.

    :param Session db: The database session.
    :param DataContractCreate data_contract: The data contract to be created.
    :return DataContract: The created data contract.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        created_data_contract = DataContract.model_validate(data_contract.model_dump())
        db_data_contract = pydantic_to_db_model(created_data_contract)
        db.add(db_data_contract)
        db.commit()
        db.refresh(db_data_contract)
    except SQLAlchemyError:
        db.rollback()
        logger.exception(" ❌ Failed to create data contract")
        raise
    except Exception:
        logger.exception(" ❌ Unexpected error occurred while creating data contract")
        raise
    else:
        logger.info(f" ✅ Data contract created successfully: {db_data_contract.id}")
        return created_data_contract


def get_data_contract(db: Session, id: str) -> DataContract | None:
    """
    Retrieves a data contract from the database by its ID.

    :param Session db: The database session.
    :param str id: The unique identifier of the data contract to retrieve.
    :return Optional[DataContract]: The retrieved data contract, or None if not found.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contract = db.query(DataContractModel).filter_by(id=id).first()
        if db_data_contract is None:
            logger.warning(f" ⚠️ Data contract not found: {id}")
            return None
    except SQLAlchemyError:
        logger.exception(" ❌ Failed to retrieve data contract")
        raise
    except Exception:
        logger.exception(" ❌ Unexpected error occurred while retrieving data contract")
        raise
    else:
        data_contract = db_to_pydantic_model(db_data_contract)
        logger.info(f" ✅ Data contract retrieved successfully: {id}")
        return data_contract


def update_data_contract(
    db: Session, id: str, data_contract_update: DataContractUpdate
) -> DataContract | None:
    """
    Updates an existing data contract in the database.

    :param Session db: The database session.
    :param str id: The unique identifier of the data contract to update.
    :param DataContractUpdate data_contract_update: The data contract update information.
    :return Optional[DataContract]: The updated data contract, or None if not found.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        updated_data_contract = DataContract.model_validate(
            data_contract_update.model_dump(exclude_unset=True)
        )
        updated_data_contract_db = pydantic_to_db_model(updated_data_contract)

        db_data_contract = db.query(DataContractModel).filter_by(id=id).first()
        if db_data_contract is None:
            logger.warning(f" ⚠️ Data contract not found for update: {id}")
            return None

        for key, value in updated_data_contract_db.__dict__.items():
            if hasattr(db_data_contract, key) and key[0] != "_":
                setattr(db_data_contract, key, value)
            else:
                logger.warning(f" ⚠️ Attribute {key} not found in DataContractModel")
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception(" ❌ Failed to update data contract")
        raise
    except Exception:
        logger.exception(" ❌ Unexpected error occurred while updating data contract")
        raise
    else:
        logger.info(f" ✅ Data contract updated successfully: {id}")
        return updated_data_contract


def list_data_contracts(db: Session) -> list[DataContract]:
    """
    Retrieves all data contracts from the database.

    :param Session db: The database session.
    :return List[DataContract]: A list of all data contracts.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contracts = db.query(DataContractModel).all()
    except SQLAlchemyError:
        logger.exception(" ❌ Failed to retrieve data contracts")
        raise
    except Exception:
        logger.exception(" ❌ Unexpected error occurred while retrieving data contracts")
        raise
    else:
        data_contracts = [db_to_pydantic_model(db_contract) for db_contract in db_data_contracts]
        logger.info(f" ✅ Retrieved {len(data_contracts)} data contracts successfully")
        return data_contracts


def delete_data_contract(
    db: Session, data_contract_delete: DataContractDelete
) -> DataContract | None:
    """
    Deletes a data contract from the database.

    :param Session db: The database session.
    :param DataContractDelete data_contract_delete: The data contract to be deleted.
    :return Optional[DataContract]: The deleted data contract, or None if not found.
    :raises SQLAlchemyError: If there's an error during database operations.
    :raises Exception: If there's any other unexpected error.
    """
    try:
        db_data_contract = db.query(DataContractModel).filter_by(id=data_contract_delete.id).first()
        if db_data_contract is None:
            logger.warning(f" ⚠️ Data contract not found for deletion: {data_contract_delete.id}")
            return None

        deleted_data_contract = db_to_pydantic_model(db_data_contract)
        db.delete(db_data_contract)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception(" ❌ Failed to delete data contract")
        raise
    except Exception:
        logger.exception(" ❌ Unexpected error occurred while deleting data contract")
        raise
    else:
        logger.info(f" ✅ Data contract deleted successfully: {data_contract_delete.id}")
        return deleted_data_contract
