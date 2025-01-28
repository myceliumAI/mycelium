import uuid

import pytest
from sqlalchemy.orm import Session

from app.crud.data_contract import DataContractCRUD
from app.exceptions.crud.data_contract import (
    DataContractNotFoundError,
)
from app.schemas.data_contract.objects.contact_object import ContactObject
from app.schemas.data_contract.objects.info_object import InfoObject
from app.schemas.data_contract.routes.data_contract_create import DataContractCreate
from app.schemas.data_contract.routes.data_contract_delete import DataContractDelete


@pytest.fixture
def data_contract_crud() -> DataContractCRUD:
    """Creates a DataContractCRUD instance for testing."""
    return DataContractCRUD()


@pytest.fixture
def sample_data_contract() -> DataContractCreate:
    """Creates a sample data contract for testing."""
    return DataContractCreate(
        data_contract_specification="1.0.0",
        id=f"test-contract-{uuid.uuid4()}",
        info=InfoObject(
            title="Test Contract",
            version="1.0.0",
            description="Test description",
            owner="Test Team",
            contact=ContactObject(name="Test Contact", email="test@example.com"),
        ),
    )


class TestDataContractCRUD:
    """Test suite for Data Contract CRUD operations."""

    def test_create_data_contract(
        self,
        db_session: Session,
        data_contract_crud: DataContractCRUD,
        sample_data_contract: DataContractCreate,
    ) -> None:
        """Test creating a new data contract."""
        created = data_contract_crud.create_data_contract(db_session, sample_data_contract)
        assert created.id == sample_data_contract.id
        assert created.info.title == sample_data_contract.info.title

    def test_get_data_contract(
        self,
        db_session: Session,
        data_contract_crud: DataContractCRUD,
        sample_data_contract: DataContractCreate,
    ) -> None:
        """Test retrieving a data contract."""
        created = data_contract_crud.create_data_contract(db_session, sample_data_contract)
        retrieved = data_contract_crud.get_data_contract(db_session, created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.info.title == created.info.title

    def test_get_nonexistent_data_contract(
        self, db_session: Session, data_contract_crud: DataContractCRUD
    ) -> None:
        """Test retrieving a non-existent data contract raises DataContractNotFoundError."""
        with pytest.raises(DataContractNotFoundError) as exc_info:
            data_contract_crud.get_data_contract(db_session, "nonexistent-id")

        assert str(exc_info.value) == " ❌ Data contract with id 'nonexistent-id' not found"

    def test_update_data_contract(
        self,
        db_session: Session,
        data_contract_crud: DataContractCRUD,
        sample_data_contract: DataContractCreate,
    ) -> None:
        """Test updating a data contract."""
        created = data_contract_crud.create_data_contract(db_session, sample_data_contract)

        updated_info = InfoObject(
            **{**sample_data_contract.info.model_dump(), "title": "Updated Title"}
        )
        update_data = DataContractCreate(
            **{**sample_data_contract.model_dump(), "info": updated_info}
        )

        updated = data_contract_crud.update_data_contract(db_session, created.id, update_data)
        assert updated is not None
        assert updated.info.title == "Updated Title"

    def test_delete_data_contract(
        self,
        db_session: Session,
        data_contract_crud: DataContractCRUD,
        sample_data_contract: DataContractCreate,
    ) -> None:
        """Test deleting a data contract."""
        created = data_contract_crud.create_data_contract(db_session, sample_data_contract)
        delete_request = DataContractDelete(id=created.id)
        deleted = data_contract_crud.delete_data_contract(db_session, delete_request)

        assert deleted is not None
        assert deleted.id == created.id

        with pytest.raises(DataContractNotFoundError):
            data_contract_crud.get_data_contract(db_session, created.id)

    def test_delete_nonexistent_data_contract(
        self, db_session: Session, data_contract_crud: DataContractCRUD
    ) -> None:
        """Test deleting a non-existent data contract."""
        delete_request = DataContractDelete(id="nonexistent-id")
        result = data_contract_crud.delete_data_contract(db_session, delete_request)

        assert result is None

    def test_list_data_contracts(
        self,
        db_session: Session,
        data_contract_crud: DataContractCRUD,
        sample_data_contract: DataContractCreate,
    ) -> None:
        """Test listing all data contracts."""
        # Create a data contract first
        created = data_contract_crud.create_data_contract(db_session, sample_data_contract)

        # List all data contracts
        contracts = data_contract_crud.list_data_contracts(db_session)

        assert len(contracts) >= 1
        assert any(contract.id == created.id for contract in contracts)
