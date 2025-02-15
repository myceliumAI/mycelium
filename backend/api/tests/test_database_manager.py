from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.database.dsn import PostgresDSN
from app.database.manager import DatabaseManager
from app.exceptions import DatabaseInitializationError


# Test constants
TEST_CREDENTIALS = {
    "username": "test_user",
    "password": "test_pwd",  # Using a clearly marked test password
    "database": "test_db",
    "host": "localhost",
    "port": 5432,
}


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
            username=TEST_CREDENTIALS["username"],
            password=TEST_CREDENTIALS["password"],
            database=TEST_CREDENTIALS["database"],
            host=TEST_CREDENTIALS["host"],
            port=TEST_CREDENTIALS["port"],
        )

        # Execute and verify
        db_manager.create_database()
        mock_engine.connect.assert_called_once()

    def test_get_db_session(self, mocker, db_session) -> None:
        """
        Test database session creation.
        Verifies that get_db returns a valid SQLAlchemy Session object.
        """
        db_manager = DatabaseManager()
        db_manager.engine = MagicMock()
        db_manager.SessionLocal = MagicMock(return_value=db_session)

        session = db_manager.get_db()
        assert isinstance(session, Session)
        assert session == db_session

    def test_setup_engine_with_invalid_credentials(
        self,
        mocker,
        db_manager: DatabaseManager,
    ) -> None:
        """Test engine setup with invalid credentials raises appropriate error."""
        error = OperationalError("mock error", None, None)

        mocker.patch("app.database.manager.create_engine", side_effect=error)

        db_manager.dsn = PostgresDSN(
            username=TEST_CREDENTIALS["username"],
            password=TEST_CREDENTIALS["password"],
            database="invalid_db",
            host="invalid_host",
            port=5432,
        )

        with pytest.raises(OperationalError) as exc_info:
            db_manager.setup_engine()

        assert str(exc_info.value) == str(error)

    def test_get_db_session_no_engine(self, mocker) -> None:
        """
        Test get_db when engine is not initialized.
        Should raise DatabaseInitializationError.
        """
        db_manager = DatabaseManager()
        db_manager.engine = None
        db_manager.SessionLocal = MagicMock()

        with pytest.raises(DatabaseInitializationError):
            db_manager.get_db()

    def test_get_db_session_no_session_local(self, mocker) -> None:
        """
        Test get_db when SessionLocal is not initialized.
        Should raise DatabaseInitializationError.
        """
        db_manager = DatabaseManager()
        db_manager.engine = MagicMock()
        db_manager.SessionLocal = None

        with pytest.raises(DatabaseInitializationError):
            db_manager.get_db()

    def test_get_db_session_operational_error(self, mocker) -> None:
        """
        Test get_db when an OperationalError occurs.
        Should close the session and re-raise the error.
        """
        db_manager = DatabaseManager()
        db_manager.engine = MagicMock()

        mock_session = MagicMock()
        db_manager.SessionLocal = MagicMock(return_value=mock_session)

        # Mock the text function
        mock_text = mocker.patch("app.database.manager.text")
        mock_text.return_value = "SELECT 1"  # Simulating the SQL text object

        # Make the session raise an OperationalError when trying to use it
        mock_session.execute = MagicMock(side_effect=OperationalError("mock error", None, None))

        with pytest.raises(OperationalError):
            db_manager.get_db()

        # Verify the session was closed
        mock_session.close.assert_called_once()

        # Verify execute was called with the right SQL
        mock_session.execute.assert_called_once_with("SELECT 1")
