import logging
from typing import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

from ..utils.config import settings
from .dsn import PostgresDSN

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(settings.LOG_LEVEL)


class DatabaseManager:
    """
    Manages PostgreSQL database operations including connection pooling, table setup, and session handling.

    This class implements the Singleton pattern to ensure only one instance
    of DatabaseManager is created throughout the application's lifecycle.
    """

    _instance = None
    Base: DeclarativeMeta = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the DatabaseManager with PostgreSQL-specific connection pooling.
        """
        if not hasattr(self, "initialized"):
            # Initialize DSN from settings
            self.dsn = PostgresDSN.from_settings()

            if not self.dsn.get_connection_url().startswith("postgresql://"):
                raise ValueError(" ❌ Only PostgreSQL databases are supported")

            self.engine = None
            self.SessionLocal = None
            self.initialized = True
            logger.info(" 💡 DatabaseManager initialized")

    def create_database(self) -> None:
        """
        Creates the database if it doesn't exist.
        Uses a temporary connection to 'postgres' database to create the target database.
        """
        db_name = self.dsn.database

        # Create a new DSN instance for postgres
        postgres_dsn = PostgresDSN(
            username=self.dsn.username,
            password=self.dsn.password,
            database="postgres",
            host=self.dsn.host,
            port=self.dsn.port,
            unix_socket=self.dsn.unix_socket,
            options=getattr(self.dsn, "options", {}),  # Safely get options or empty dict
        )

        temp_engine = create_engine(postgres_dsn.get_connection_url())

        try:
            with temp_engine.connect() as conn:
                conn.execute(text("commit"))
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                logger.info(" ✅ Database created successfully")
        except ProgrammingError:
            logger.info(" ❎ Database already exists")
        finally:
            temp_engine.dispose()

    def setup_engine(self) -> None:
        """
        Sets up the database engine with optimized settings for PostgreSQL.
        Configures connection pooling with recommended PostgreSQL settings.
        """
        try:
            self.create_database()
        except Exception as e:
            logger.warning(f" ⚠️ Could not create database: {str(e)}")
        self.engine = create_engine(
            self.dsn.get_connection_url(),
            echo=False,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            isolation_level="READ COMMITTED",
        )

        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_connection, connection_record):
            logger.info(" ✅ New database connection established")

        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            logger.debug(" 💡 Connection checked out from pool")

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        logger.info(" ✅ Database engine setup completed")

    def create_tables(self) -> None:
        """
        Creates all tables defined in the SQLAlchemy models.

        :raises RuntimeError: If the database engine is not initialized
        :raises Exception: If table creation fails
        """
        if not self.engine:
            raise RuntimeError(" ❌ Database engine not initialized. Call setup_engine() first.")

        try:
            self.Base.metadata.create_all(bind=self.engine)
            logger.info(" ✅ Database tables created successfully")
        except Exception:
            logger.error(" ❌ Failed to create database tables")
            raise

    def get_db(self) -> Generator[Session, None, None]:
        """
        Creates a new database session with connection management.

        :yield: A SQLAlchemy Session object
        :raises RuntimeError: If the database engine is not initialized
        :raises OperationalError: If database operations fail
        """
        if not self.engine or not self.SessionLocal:
            raise RuntimeError(" ❌ Database engine not initialized. Call setup_engine() first.")

        db = self.SessionLocal()
        try:
            logger.debug(" 💡 New database session created")
            yield db
        except OperationalError as e:
            logger.error(f" ❌ Database operation failed: {str(e)}")
            raise
        finally:
            db.close()
            logger.debug(" 💡 Database session closed")


# Singleton instance
db_manager = DatabaseManager()
