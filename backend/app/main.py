import importlib
import logging
import os
from typing import Any, Dict, List, Tuple

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database.manager import db_manager
from .utils.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class AppManager:
    """
    Manages the FastAPI application setup and configuration.
    """

    def __init__(self):
        self.setup_database()
        self.app = FastAPI(
            title="Mycelium API",
            description="An API for managing data contracts and related operations.",
            version="1.0.0",
        )
        self.configure_cors()
        self.include_routers()
        self.setup_health_check()

    def setup_database(self) -> None:
        """
        Sets up the database by creating an instance of DatabaseManager,
        creating the database, and setting up the engine.
        """
        try:
            db_manager.create_database()
            db_manager.setup_engine()
            self.import_models()
            db_manager.create_tables()
            logger.info(" ✅ Database setup completed successfully")
        except Exception as e:
            logger.error(f" ❌ Error setting up the database: {e}")

    def import_models(self) -> None:
        """
        Imports all model classes from the 'models' directory.

        This method is crucial for establishing the link between SQLAlchemy models and the database.
        By importing the models, we ensure that SQLAlchemy's declarative base is aware of all model
        classes before creating the tables. This step is necessary because SQLAlchemy uses the
        imported models to generate the database schema.
        """
        try:
            models_dir = os.path.join(os.path.dirname(__file__), "models")
            for filename in os.listdir(models_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = f".models.{filename[:-3]}"
                    importlib.import_module(module_name, package=__package__)
            logger.info(" ✅ All models imported successfully")
        except Exception as e:
            logger.error(f" ❌ Error importing models: {e}")

    def configure_cors(self) -> None:
        """
        Configures CORS middleware for the FastAPI application.
        """
        try:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOWED_ORIGINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            logger.info(" ✅ CORS middleware configured successfully")
        except Exception as e:
            logger.error(f" ❌ Error configuring CORS middleware: {e}")

    def import_routers(self) -> List[Tuple[APIRouter, str]]:
        """
        Dynamically imports and returns a list of routers from the 'routers' directory.

        :return List[Tuple[APIRouter, str]]: A list of tuples containing imported routers and their names.
        """
        routers = []
        try:
            routers_dir = os.path.join(os.path.dirname(__file__), "routers")
            for filename in os.listdir(routers_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = f".routers.{filename[:-3]}"
                    module = importlib.import_module(module_name, package=__package__)
                    if hasattr(module, "router"):
                        routers.append((module.router, filename[:-3]))
            return routers
        except Exception as e:
            import traceback

            traceback.print_exc()
            logger.error(f" ❌ Error importing routers: {e}")
            return []

    def include_routers(self) -> None:
        """
        Includes all imported routers in the FastAPI application.
        """
        try:
            for router, name in self.import_routers():
                tag = name.replace("_", " ").title()
                self.app.include_router(router, prefix=f"/{name}", tags=[tag])
            logger.info(" ✅ All routers included successfully")
        except Exception as e:
            logger.error(f" ❌ Error including routers: {e}")

    def setup_health_check(self) -> None:
        """
        Sets up the health check endpoint for the application.
        """

        @self.app.get("/health", tags=["Health"])
        async def health_check() -> Dict[str, Any]:
            """
            Checks the health status of the application.

            :return Dict[str, Any]: Health status information including database connectivity
            """
            try:
                # Test database connection
                db_manager.engine.connect()
                return JSONResponse(
                    content={"status": "healthy"},
                    status_code=200,
                )
            except Exception as e:
                logger.error(f" ❌ Health check failed: {str(e)}")
                return JSONResponse(
                    content={"status": "unhealthy"},
                    status_code=503,
                )


app_manager = AppManager()
app = app_manager.app
