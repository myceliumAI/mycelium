from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import OperationalError

from app.database.dsn import PostgresDSN
from app.database.manager import DatabaseManager


class TestDatabaseManager:
    """Test suite for DatabaseManager class."""

    @pytest.fixture
    def db_manager(self) -> DatabaseManager:
        """Create a DatabaseManager instance for testing."""
        return DatabaseManager()

    def test_singleton_pattern(self, db_manager: DatabaseManager) -> None:
        """Test that DatabaseManager follows singleton pattern."""
        db2 = DatabaseManager()
        assert db_manager is db2, "DatabaseManager instances should be identical (singleton)"

    def test_create_database_success(self, mocker, db_manager: DatabaseManager) -> None:
        """Test successful database creation."""
        # Mock setup
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mocker.patch("app.database.manager.create_engine", return_value=mock_engine)

        # Test configuration
        db_manager.dsn = PostgresDSN(
            username="test", password="test", database="test_db", host="localhost", port=5432
        )

        # Execute and verify
        db_manager.create_database()
        mock_engine.connect.assert_called_once()

    def test_get_db_session(self, mocker, db_session) -> None:
        """Test database session creation and cleanup."""
        db_manager = DatabaseManager()
        db_manager.engine = MagicMock()
        db_manager.SessionLocal = MagicMock(return_value=db_session)

        session_generator = db_manager.get_db()
        assert isinstance(session_generator, Generator)
        session = next(session_generator)
        assert session == db_session

    def test_setup_engine_with_invalid_credentials(
        self, mocker, db_manager: DatabaseManager
    ) -> None:
        """Test engine setup with invalid credentials raises appropriate error."""
        error_message = "mock connection error"
        error = OperationalError("mock error", None, None)

        mocker.patch("app.database.manager.create_engine", side_effect=error)

        db_manager.dsn = PostgresDSN(
            username="invalid",
            password="invalid",
            database="invalid_db",
            host="invalid_host",
            port=5432,
        )

        with pytest.raises(OperationalError) as exc_info:
            db_manager.setup_engine()

        assert str(exc_info.value) == str(error)
