from unittest.mock import MagicMock, patch
import pytest
from sqlalchemy.exc import OperationalError
from app.database.manager import DatabaseManager
from app.database.dsn import PostgresDSN

class TestDatabaseManager:
    """Test suite for DatabaseManager class."""

    def test_singleton_pattern(self):
        """Test that DatabaseManager follows singleton pattern."""
        db1 = DatabaseManager()
        db2 = DatabaseManager()
        assert db1 is db2

    def test_create_database_success(self, mocker):
        """Test successful database creation."""
        # Complete mock of create_engine and its connection chain
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Mock create_engine at the right location
        mocker.patch('app.database.manager.create_engine', return_value=mock_engine)
        
        db_manager = DatabaseManager()
        db_manager.dsn = PostgresDSN(
            username="test",
            password="test",
            database="test_db",
            host="localhost",
            port=5432
        )
        
        db_manager.create_database()
        mock_engine.connect.assert_called_once()

    def test_get_db_session(self, mocker, db_session):
        """Test database session creation and cleanup."""
        db_manager = DatabaseManager()
        # Initialize the engine before using get_db
        db_manager.engine = MagicMock()
        db_manager.SessionLocal = MagicMock(return_value=db_session)
        
        session_generator = db_manager.get_db()
        session = next(session_generator)
        assert session == db_session

    def test_setup_engine_with_invalid_credentials(self, mocker):
        """Test engine setup with invalid credentials."""
        error = OperationalError("mock error", None, None)
        
        # Mock create_engine at the right location and for the right method
        mocker.patch('app.database.manager.create_engine', side_effect=error)
        
        db_manager = DatabaseManager()
        db_manager.dsn = PostgresDSN(
            username="invalid",
            password="invalid",
            database="invalid_db",
            host="invalid_host",
            port=5432
        )
        
        # Test should raise the exception when calling setup_engine
        with pytest.raises(OperationalError) as exc_info:
            db_manager.setup_engine()
            
        assert str(exc_info.value) == str(error) 