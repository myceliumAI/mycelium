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
        self.POSTGRES_HOST: Optional[str] = self._get_env("POSTGRES_HOST")
        self.POSTGRES_SOCKET: Optional[str] = self._get_env("POSTGRES_SOCKET")
        self.POSTGRES_PORT: Optional[int] = self._get_port("POSTGRES_PORT")

        # Security settings
        self.ALLOWED_HOSTS: List[str] = self._get_required_env("ALLOWED_HOSTS", "*").split(",")

        # CORS settings
        self.ALLOWED_ORIGINS: List[str] = self._get_required_env("ALLOWED_ORIGINS", "*").split(",")

        # Other settings
        self.LOG_LEVEL: Final[str] = self._get_required_env("LOG_LEVEL", "INFO")
        self.ALGORITHM: Final[str] = "HS256"

    def _get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable, converting empty strings to None.

        :param str key: The environment variable key
        :param Optional[str] default: The default value if the environment variable is not set
        :return Optional[str]: The environment variable value or None
        """
        value = getenv(key, default)
        return value if value and value.strip() else None

    def _get_port(self, key: str) -> Optional[int]:
        """
        Get and convert port number from environment variable.

        :param str key: Environment variable key
        :return Optional[int]: Port number if set, None otherwise
        :raises ValueError: If port is not a valid number
        """
        value = self._get_env(key)
        if value is not None:
            try:
                return int(value)
            except ValueError:
                raise ValueError(f" ❌ Invalid port number for {key}: {value}")
        return None

    def _get_required_env(self, key: str, default: Optional[str] = None) -> str:
        """
        Get a required environment variable.

        :param str key: The environment variable key
        :param Optional[str] default: The default value if the environment variable is not set
        :return str: The environment variable value
        :raises ValueError: If the environment variable is not set or empty and no default provided
        """
        value = self._get_env(key, default)
        if value is None:
            raise ValueError(f" ❌ Required environment variable {key} is not set or empty")
        return value


settings = Settings()
