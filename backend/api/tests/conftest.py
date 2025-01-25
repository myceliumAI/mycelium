import os
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.manager import db_manager
from app.utils.config import settings

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    monkeypatch.setattr(settings, "POSTGRES_USER", "test_user")
    monkeypatch.setattr(settings, "POSTGRES_PASSWORD", "test_password")
    monkeypatch.setattr(settings, "POSTGRES_DB", "test_db")
    monkeypatch.setattr(settings, "POSTGRES_HOST", "localhost")
    monkeypatch.setattr(settings, "POSTGRES_PORT", 5432)
    monkeypatch.setattr(settings, "POSTGRES_SOCKET", None)

@pytest.fixture(scope="session")
def test_db_url() -> str:
    """Returns a SQLite URL for testing."""
    return "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine(test_db_url: str):
    """Creates a SQLite engine for testing."""
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    db_manager.Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture
def db_session(test_engine) -> Session:
    """Create a new database session for testing."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db_session: Session) -> TestClient:
    """Create a new FastAPI TestClient."""
    # Import app ici pour éviter l'initialisation précoce
    from app.main import app
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[db_manager.get_db] = override_get_db
    
    # Utiliser SQLite pour les tests
    db_manager.engine = db_session.bind
    db_manager.SessionLocal = sessionmaker(bind=db_session.bind)
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def setup_test_db(test_engine):
    """Configure la base de données de test."""
    # Créer les tables
    db_manager.Base.metadata.create_all(bind=test_engine)
    
    # Configurer le gestionnaire de base de données pour les tests
    db_manager.engine = test_engine
    db_manager.SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    
    yield
    
    # Nettoyer après les tests
    db_manager.Base.metadata.drop_all(bind=test_engine) 