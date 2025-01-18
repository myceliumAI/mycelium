import logging
from os import getenv
from typing import Final, List, Optional

logger = logging.getLogger(__name__)


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
        self.POSTGRES_USER: Final[str] = self._get_required_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD: Final[str] = self._get_required_env("POSTGRES_PASSWORD")
        self.POSTGRES_DB: Final[str] = self._get_required_env("POSTGRES_DB")
        self.POSTGRES_HOST: Optional[str] = getenv("POSTGRES_HOST")
        self.POSTGRES_SOCKET: Optional[str] = getenv("POSTGRES_SOCKET")
        self.POSTGRES_PORT: Optional[int] = self._get_port("POSTGRES_PORT")

        # Security settings
        self.ALLOWED_HOSTS: List[str] = self._get_required_env("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

        # CORS settings
        self.ALLOWED_ORIGINS: List[str] = self._get_required_env("ALLOWED_ORIGINS", "*").split(",")

        # Other settings
        self.LOG_LEVEL: Final[str] = self._get_required_env("LOG_LEVEL", "INFO")
        self.ALGORITHM: Final[str] = "HS256"

    def _get_port(self, key: str) -> Optional[int]:
        """
        Get and convert port number from environment variable.

        :param str key: Environment variable key
        :return Optional[int]: Port number if set, None otherwise
        :raises ValueError: If port is not a valid number
        """
        port = getenv(key)
        if port is not None:
            try:
                return int(port)
            except ValueError:
                raise ValueError(f" ❌ Invalid port number for {key}: {port}")
        return None

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
