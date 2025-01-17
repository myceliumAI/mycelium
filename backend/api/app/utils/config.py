from os import getenv
from pathlib import Path
from typing import Final, List, Optional


class Settings:
    """
    Configuration settings for the application.

    This class holds the configuration settings for the application, including
    database connection details, LLM API information, and server configuration.
    It uses environment variables with default values.

    :raises ValueError: If required environment variables are not set
    """

    def __init__(self):
        """Initialize settings and validate required environment variables."""
        # Database configuration
        postgres_user = self._get_required_env("POSTGRES_USER")
        postgres_password = self._get_required_env("POSTGRES_PASSWORD")
        postgres_db = self._get_required_env("POSTGRES_DB")
        postgres_host = getenv("POSTGRES_HOST")
        postgres_socket = getenv("POSTGRES_SOCKET")
        postgres_port = getenv("POSTGRES_PORT")
        # Build database URL based on connection type
        if postgres_socket:
            socket_dir = Path(postgres_socket).parent
            self.DATABASE_URL: Final[str] = (
                f"postgresql://{postgres_user}:{postgres_password}@/"
                f"{postgres_db}?host={socket_dir}"
            )
        else:
            self.DATABASE_URL: Final[str] = (
                f"postgresql://{postgres_user}:{postgres_password}@"
                f"{postgres_host}:{postgres_port}/{postgres_db}"
            )

        # Security settings
        self.ALLOWED_HOSTS: List[str] = self._get_required_env(
            "ALLOWED_HOSTS", 
            "localhost,127.0.0.1"
        ).split(",")
        
        # CORS settings
        self.ALLOWED_ORIGINS: List[str] = self._get_required_env(
            "ALLOWED_ORIGINS", 
            "*"
        ).split(",")

        # Other settings
        self.LOG_LEVEL: Final[str] = self._get_required_env("LOG_LEVEL", "INFO")
        self.ALGORITHM: Final[str] = "HS256"

    def _get_required_env(self, key: str, default: Optional[str] = None) -> str:
        """
        Get a required environment variable.

        :param str key: The environment variable key
        :param Optional[str] default: The default value if the environment variable is not set
        :return str: The environment variable value
        :raises ValueError: If the environment variable is not set and no default provided
        """
        value = getenv(key, default)
        if value is None:
            raise ValueError(f" ❌ Required environment variable {key} is not set")
        return value


settings = Settings()
