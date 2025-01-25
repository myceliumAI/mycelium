import importlib
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .database.manager import db_manager
from .utils.config import settings


# Configure logging with proper format
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AppManager:
    """
    Manages the FastAPI application setup and configuration.
    """

    def __init__(self) -> None:
        """
        Initialize the application with all necessary security measures and configurations.
        """
        self._routers_cache: list[tuple[APIRouter, str]] | None = None
        try:
            self._setup_directories()
            self.setup_database()

            self.app = FastAPI(
                title="Mycelium API",
                description="An API for managing data contracts and related operations.",
                version="1.0.0",
            )

            self._configure_middleware()
            self.include_routers()
            self.setup_health_check()

            logger.info(" ✅ Application initialized successfully")
        except Exception as e:
            logger.critical(" 🔥 Critical error during application initialization")
            raise e from None

    @staticmethod
    def _ensure_directory_exists(directory: Path) -> None:
        """
        Safely create directory if it doesn't exist with proper permissions.
        :param Path directory: Path object representing the directory to create
        """
        try:
            if not directory.exists():
                directory.mkdir(parents=True, mode=0o750)  # Secure permissions
                logger.info(f" ✅ Created directory: {directory}")
        except Exception:
            logger.exception(f" ❌ Failed to create directory {directory}")
            raise

    def _setup_directories(self) -> None:
        """
        Set up all required application directories with proper permissions.
        """
        app_dir = Path(__file__).parent
        directories = [app_dir / "assets" / "templates", app_dir / "logs", app_dir / "temp"]

        for directory in directories:
            self._ensure_directory_exists(directory)

    def _configure_middleware(self) -> None:
        """
        Configure all application middleware with secure defaults.
        """
        try:
            # CORS configuration with strict settings
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOWED_ORIGINS,
                allow_credentials=True,
                allow_methods=["GET", "POST", "PUT", "DELETE"],
                allow_headers=["*"],
                max_age=3600,
            )

            # Add trusted host middleware
            self.app.add_middleware(
                TrustedHostMiddleware,
                allowed_hosts=settings.ALLOWED_HOSTS,
            )

            # Add compression middleware
            self.app.add_middleware(GZipMiddleware, minimum_size=1000)

            logger.info(" ✅ Middleware configured successfully")
        except Exception:
            logger.exception(" ❌ Error configuring middleware")
            raise

    def _get_routers(self) -> list[tuple[APIRouter, str]]:
        """
        Get and cache the list of routers.
        :return List[Tuple[APIRouter, str]]: List of tuples containing router instances and their names
        """
        if self._routers_cache is None:
            routers = []
            try:
                routers_dir = Path(__file__).parent / "routers"
                for file in routers_dir.glob("*.py"):
                    if file.stem.startswith("__"):
                        continue

                    try:
                        module = importlib.import_module(
                            f".routers.{file.stem}", package=__package__
                        )
                        if hasattr(module, "router"):
                            routers.append((module.router, file.stem))
                    except Exception:
                        logger.exception(f" ❌ Error importing router {file.stem}")
                        continue

                self._routers_cache = routers
            except Exception:
                logger.exception(" ❌ Error scanning routers directory")
                return []

        return self._routers_cache

    def setup_database(self) -> None:
        """
        Set up database with proper error handling and connection pooling.
        """
        try:
            db_manager.create_database()
            db_manager.setup_engine()
            self.import_models()
            db_manager.create_tables()
            logger.info(" ✅ Database setup completed successfully")
        except Exception:
            logger.exception(" ❌ Database setup failed")
            raise

    def import_models(self) -> None:
        """
        Import all models with proper error handling.
        """
        try:
            models_dir = Path(__file__).parent / "models"
            for file in models_dir.glob("*.py"):
                if not file.stem.startswith("__"):
                    importlib.import_module(f".models.{file.stem}", package=__package__)
            logger.info(" ✅ Models imported successfully")
        except Exception:
            logger.exception(" ❌ Error importing models")
            raise

    def include_routers(self) -> None:
        """
        Include routers with proper error handling and logging.
        """
        try:
            for router, name in self._get_routers():
                tag = name.replace("_", " ").title()
                self.app.include_router(
                    router,
                    prefix=f"/{name}",
                    tags=[tag],
                )
            logger.info(" ✅ Routers included successfully")
        except Exception:
            logger.exception(" ❌ Error including routers")
            raise

    def setup_health_check(self) -> None:
        """
        Set up health check endpoint with comprehensive checks.
        """

        @self.app.get("/health", tags=["Health"])
        async def health_check() -> dict[str, Any]:
            """
            Comprehensive health check endpoint that verifies system components.
            :return Dict[str, Any]: Health status including various system checks
            """
            try:
                # Test database connection using SQLAlchemy text()
                with db_manager.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    conn.commit()

                # Check template directory
                template_dir = Path(__file__).parent / "assets" / "templates"
                templates_ok = template_dir.exists() and template_dir.is_dir()

                return JSONResponse(
                    content={
                        "status": "healthy",
                        "database": "connected",
                        "templates_directory": "ok" if templates_ok else "error",
                        "version": "1.0.0",
                    },
                    status_code=200,
                )
            except Exception:
                logger.exception(" ❌ Health check failed")
                return JSONResponse(
                    content={
                        "status": "unhealthy",
                        "code": "SERVICE_UNAVAILABLE",
                    },
                    status_code=503,
                )


# Singleton instance
app_manager = AppManager()
app = app_manager.app
