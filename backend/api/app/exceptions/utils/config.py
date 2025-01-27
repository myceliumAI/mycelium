"""Configuration related error classes."""

from typing import Any


class ConfigError(Exception):
    """Base exception class for configuration errors."""

    pass


class InvalidPortError(ConfigError):
    """Exception raised when a port number is invalid."""

    def __init__(self, key: str, value: Any):
        self.message = f" ❌ Invalid port number for {key}: {value}"
        super().__init__(self.message)


class MissingEnvironmentVariableError(ConfigError):
    """Exception raised when a required environment variable is missing."""

    def __init__(self, key: str):
        self.message = f" ❌ Required environment variable {key} is not set or empty"
        super().__init__(self.message)
