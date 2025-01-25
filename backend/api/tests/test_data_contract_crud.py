import uuid

import pytest
from sqlalchemy.orm import Session

from app.crud.data_contract import (
    create_data_contract,
    delete_data_contract,
    get_data_contract,
    update_data_contract,
)
from app.schemas.data_contract.objects.contact_object import ContactObject
from app.schemas.data_contract.objects.info_object import InfoObject
from app.schemas.data_contract.routes.data_contract_create import DataContractCreate
from app.schemas.data_contract.routes.data_contract_delete import DataContractDelete


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
        self, db_session: Session, sample_data_contract: DataContractCreate
    ) -> None:
        """Test creating a new data contract."""
        created = create_data_contract(db_session, sample_data_contract)
        assert created.id == sample_data_contract.id
        assert created.info.title == sample_data_contract.info.title

    def test_get_data_contract(
        self, db_session: Session, sample_data_contract: DataContractCreate
    ) -> None:
        """Test retrieving a data contract."""
        created = create_data_contract(db_session, sample_data_contract)
        retrieved = get_data_contract(db_session, created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.info.title == created.info.title

    def test_get_nonexistent_data_contract(self, db_session: Session) -> None:
        """Test retrieving a non-existent data contract returns None."""
        retrieved = get_data_contract(db_session, "nonexistent-id")
        assert retrieved is None

    def test_update_data_contract(
        self, db_session: Session, sample_data_contract: DataContractCreate
    ) -> None:
        """Test updating a data contract."""
        created = create_data_contract(db_session, sample_data_contract)

        updated_info = InfoObject(
            **{**sample_data_contract.info.model_dump(), "title": "Updated Title"}
        )
        update_data = DataContractCreate(
            **{**sample_data_contract.model_dump(), "info": updated_info}
        )

        updated = update_data_contract(db_session, created.id, update_data)
        assert updated is not None
        assert updated.info.title == "Updated Title"

    def test_delete_data_contract(
        self, db_session: Session, sample_data_contract: DataContractCreate
    ) -> None:
        """Test deleting a data contract."""
        created = create_data_contract(db_session, sample_data_contract)
        delete_request = DataContractDelete(id=created.id)
        deleted = delete_data_contract(db_session, delete_request)

        assert deleted is not None
        assert deleted.id == created.id

        # Verify deletion
        retrieved = get_data_contract(db_session, created.id)
        assert retrieved is None
