from contextlib import contextmanager
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.exceptions.crud.data_contract import (
    DataContractNotFoundError,
)
from app.models.data_contract import DataContract as DataContractModel
from app.schemas.data_contract.objects.contact_object import ContactObject
from app.schemas.data_contract.objects.data_contract import DataContract
from app.schemas.data_contract.objects.info_object import InfoObject
from app.schemas.data_contract.routes.data_contract_create import DataContractCreate
from app.schemas.data_contract.routes.data_contract_delete import DataContractDelete
from app.schemas.data_contract.routes.data_contract_update import DataContractUpdate
from app.services.data_contract import DataContractService


@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    session = MagicMock()

    # Configuration du mock pour la méthode query
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_first = MagicMock()

    mock_query.filter_by.return_value = mock_filter
    mock_filter.first.return_value = mock_first
    session.query.return_value = mock_query

    return session


@pytest.fixture
def mock_db(mock_db_session):
    """Mock database context manager."""

    @contextmanager
    def _mock_db():
        yield mock_db_session

    return _mock_db


@pytest.fixture
def data_contract_service() -> DataContractService:
    """Creates a DataContractService instance for testing."""
    return DataContractService()


@pytest.fixture
def sample_data_contract() -> DataContractCreate:
    """Creates a sample data contract for testing."""
    return DataContractCreate(
        data_contract_specification="1.0.0",
        id=f"test-contract-{uuid4()}",
        info=InfoObject(
            title="Test Contract",
            version="1.0.0",
            description="Test description",
            owner="Test Team",
            contact=ContactObject(name="Test Contact", email="test@example.com"),
        ),
    )


@pytest.fixture
def db_data_contract(sample_data_contract) -> DataContractModel:
    """Creates a sample database data contract model."""
    return DataContractModel(
        id=sample_data_contract.id,
        data_contract_specification=sample_data_contract.data_contract_specification,
        info=sample_data_contract.info.model_dump(),
    )


class TestDataContractService:
    """Test suite for Data Contract Service operations."""

    def test_create_data_contract(
        self,
        data_contract_service: DataContractService,
        mock_db,
        sample_data_contract: DataContractCreate,
        db_data_contract: DataContractModel,
        mock_db_session,
    ):
        """Test creating a new data contract through the service."""
        with patch("app.services.data_contract.db_manager.get_db", mock_db):
            # Setup mock
            mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
                db_data_contract
            )

            # Execute
            created = data_contract_service.create_data_contract(sample_data_contract)

            # Verify
            assert created.id == sample_data_contract.id
            assert created.info.title == sample_data_contract.info.title

    def test_get_data_contract(
        self,
        data_contract_service: DataContractService,
        mock_db,
        sample_data_contract: DataContractCreate,
        db_data_contract: DataContractModel,
        mock_db_session,
    ):
        """Test retrieving a data contract through the service."""
        with patch("app.services.data_contract.db_manager.get_db", mock_db):
            # Setup mock
            mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
                db_data_contract
            )

            # Execute
            retrieved = data_contract_service.get_data_contract(sample_data_contract.id)

            # Verify
            assert retrieved is not None
            assert retrieved.id == sample_data_contract.id
            assert retrieved.info.title == sample_data_contract.info.title

    def test_get_nonexistent_data_contract(
        self, data_contract_service: DataContractService, mock_db, mock_db_session
    ):
        """Test retrieving a non-existent data contract returns None."""
        with patch("app.services.data_contract.db_manager.get_db", mock_db):
            # Setup mock to return None
            mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

            # Execute
            with pytest.raises(DataContractNotFoundError) as exc_info:
                data_contract_service.get_data_contract("nonexistent-id")

            # Verify
            assert str(exc_info.value) == " ❌ Data contract with id 'nonexistent-id' not found"

    def test_update_data_contract(
        self,
        data_contract_service: DataContractService,
        mock_db,
        sample_data_contract: DataContractCreate,
        db_data_contract: DataContractModel,
        mock_db_session,
    ):
        """Test updating a data contract through the service."""
        with patch("app.services.data_contract.db_manager.get_db", mock_db):
            # Setup mock
            mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
                db_data_contract
            )

            # Prepare update data
            updated_info = InfoObject(
                **{**sample_data_contract.info.model_dump(), "title": "Updated Title"}
            )
            update_data = DataContractUpdate(
                **{**sample_data_contract.model_dump(), "info": updated_info}
            )

            # Execute
            updated = data_contract_service.update_data_contract(
                sample_data_contract.id, update_data
            )

            # Verify
            assert updated is not None
            assert updated.info.title == "Updated Title"

    def test_delete_data_contract(
        self,
        data_contract_service: DataContractService,
        mock_db,
        sample_data_contract: DataContractCreate,
        db_data_contract: DataContractModel,
        mock_db_session,
    ):
        """Test deleting a data contract through the service."""
        with (
            patch("app.services.data_contract.db_manager.get_db", mock_db),
            patch(
                "app.services.data_contract.DataContractCRUD.delete_data_contract"
            ) as mock_delete,
        ):
            # Setup mock pour la recherche du data contract
            mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
                db_data_contract
            )

            # Setup mock pour la suppression
            mock_delete.return_value = DataContract.model_validate(
                sample_data_contract.model_dump()
            )

            # Execute
            delete_request = DataContractDelete(id=sample_data_contract.id)
            deleted = data_contract_service.delete_data_contract(delete_request)

            # Verify
            assert deleted is not None
            assert isinstance(deleted, DataContract)
            assert deleted.id == sample_data_contract.id

            # Verify que la méthode delete a été appelée avec les bons arguments
            mock_delete.assert_called_once()

    def test_list_data_contracts(
        self,
        data_contract_service: DataContractService,
        mock_db,
        db_data_contract: DataContractModel,
        mock_db_session,
    ):
        """Test listing all data contracts through the service."""
        with patch("app.services.data_contract.db_manager.get_db", mock_db):
            # Setup mock
            mock_db_session.query.return_value.all.return_value = [db_data_contract]

            # Execute
            contracts = data_contract_service.list_data_contracts()

            # Verify
            assert len(contracts) >= 1
            assert contracts[0].id == db_data_contract.id
