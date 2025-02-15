"""Data Contract service module."""

from ..crud.data_contract import DataContractCRUD
from ..database.manager import db_manager
from ..schemas.data_contract.objects.data_contract import DataContract
from ..schemas.data_contract.routes.data_contract_create import DataContractCreate
from ..schemas.data_contract.routes.data_contract_delete import DataContractDelete
from ..schemas.data_contract.routes.data_contract_update import DataContractUpdate
from ..utils.logger import get_logger


logger = get_logger(__name__)


class DataContractService:
    """Service class for managing data contracts."""

    def __init__(self):
        """Initialize the data contract service."""
        self._crud = DataContractCRUD()

    def create_data_contract(self, data_contract: DataContractCreate) -> DataContract:
        """
        Create a new data contract.

        :param DataContractCreate data_contract: The data contract to create
        :return DataContract: The created data contract
        :raises SQLAlchemyError: If there's a database error
        :raises ValueError: If the data is invalid
        """
        with db_manager.get_db() as db:
            return self._crud.create_data_contract(db, data_contract)

    def get_data_contract(self, id: str) -> DataContract | None:
        """
        Get a data contract by its ID.

        :param str id: The ID of the data contract
        :return Optional[DataContract]: The data contract if found, None otherwise
        :raises SQLAlchemyError: If there's a database error
        """
        with db_manager.get_db() as db:
            return self._crud.get_data_contract(db, id)

    def update_data_contract(
        self,
        id: str,
        data_contract: DataContractUpdate,
    ) -> DataContract | None:
        """
        Update an existing data contract.

        :param str id: The ID of the data contract to update
        :param DataContractUpdate data_contract: The update data
        :return Optional[DataContract]: The updated data contract if found, None otherwise
        :raises SQLAlchemyError: If there's a database error
        :raises ValueError: If the data is invalid
        """
        with db_manager.get_db() as db:
            return self._crud.update_data_contract(db, id, data_contract)

    def list_data_contracts(self) -> list[DataContract]:
        """
        List all data contracts.

        :return list[DataContract]: List of all data contracts
        :raises SQLAlchemyError: If there's a database error
        """
        with db_manager.get_db() as db:
            return self._crud.list_data_contracts(db)

    def delete_data_contract(self, data_contract: DataContractDelete) -> DataContract | None:
        """
        Delete a data contract.

        :param DataContractDelete data_contract: The data contract to delete
        :return Optional[DataContract]: The deleted data contract if found, None otherwise
        :raises SQLAlchemyError: If there's a database error
        """
        with db_manager.get_db() as db:
            return self._crud.delete_data_contract(db, data_contract)


# Singleton instance
data_contract_service = DataContractService()
