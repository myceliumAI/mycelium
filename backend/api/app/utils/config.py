import logging
from os import getenv
from typing import Final


logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Base exception class for configuration errors."""

    pass


class InvalidPortError(ConfigError):
    """Exception raised when a port number is invalid."""

    def __init__(self, key: str, value: str):
        self.message = f" ❌ Invalid port number for {key}: {value}"
        super().__init__(self.message)


class MissingEnvironmentVariableError(ConfigError):
    """Exception raised when a required environment variable is missing."""

    def __init__(self, key: str):
        self.message = f" ❌ Required environment variable {key} is not set or empty"
        super().__init__(self.message)


class Settings:
    """
    Configuration settings for the application.

    This class holds the configuration settings for the application, including
    database connection details, LLM API information, and server configuration.
    It uses environment variables with default values.

    :raises ConfigError: If required environment variables are not set or are invalid
    """

    def __init__(self):
        """Initialize settings and validate required environment variables."""
        # Database configuration
        self.POSTGRES_USER: Final[str] = self._get_required_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD: Final[str] = self._get_required_env("POSTGRES_PASSWORD")
        self.POSTGRES_DB: Final[str] = self._get_required_env("POSTGRES_DB")
        self.POSTGRES_HOST: str | None = self._get_env("POSTGRES_HOST")
        self.POSTGRES_SOCKET: str | None = self._get_env("POSTGRES_SOCKET")
        self.POSTGRES_PORT: int | None = self._get_port("POSTGRES_PORT")

        # Security settings
        self.ALLOWED_HOSTS: list[str] = self._get_required_env("ALLOWED_HOSTS", "*").split(",")

        # CORS settings
        self.ALLOWED_ORIGINS: list[str] = self._get_required_env("ALLOWED_ORIGINS", "*").split(",")

        # Other settings
        self.LOG_LEVEL: Final[str] = self._get_required_env("LOG_LEVEL", "INFO")
        self.ALGORITHM: Final[str] = "HS256"

    def _get_env(self, key: str, default: str | None = None) -> str | None:
        """
        Get an environment variable, converting empty strings to None.

        :param str key: The environment variable key
        :param Optional[str] default: The default value if the environment variable is not set
        :return Optional[str]: The environment variable value or None
        """
        value = getenv(key, default)
        return value if value and value.strip() else None

    def _get_port(self, key: str) -> int | None:
        """
        Get and convert port number from environment variable.

        :param str key: Environment variable key
        :return Optional[int]: Port number if set, None otherwise
        :raises InvalidPortError: If port is not a valid number
        """
        value = self._get_env(key)
        if value is not None:
            try:
                return int(value)
            except ValueError as err:
                raise InvalidPortError(key, value) from err
        return None

    def _get_required_env(self, key: str, default: str | None = None) -> str:
        """
        Get a required environment variable.

        :param str key: The environment variable key
        :param Optional[str] default: The default value if the environment variable is not set
        :return str: The environment variable value
        :raises MissingEnvironmentVariableError: If the environment variable is not set or empty and no default provided
        """
        value = self._get_env(key, default)
        if value is None:
            raise MissingEnvironmentVariableError(key)
        return value


settings = Settings()
