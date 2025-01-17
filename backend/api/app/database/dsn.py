from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus
import logging

logger = logging.getLogger(__name__)

@dataclass
class PostgresDSN:
    """
    PostgreSQL Data Source Name configuration.
    Supports multiple connection methods: TCP, Unix Socket, and Cloud SQL.
    """
    username: str
    password: str
    database: str
    
    # TCP connection
    host: Optional[str] = None
    port: Optional[int] = None
    
    # Unix socket
    unix_socket: Optional[str] = None

    def __post_init__(self):
        """
        Validate DSN configuration after initialization.
        Checks for required credentials and connection method.
        """
        # Check credentials
        missing_credentials = []
        if not self.username:
            missing_credentials.append("username")
        if not self.password:
            missing_credentials.append("password")
        if not self.database:
            missing_credentials.append("database")
            
        if missing_credentials:
            raise ValueError(f" ❌ Missing required credentials: {', '.join(missing_credentials)}")

        # Check connection method
        has_socket = bool(self.unix_socket)
        has_tcp = bool(self.host and self.port)

        if not has_socket and not has_tcp:
            raise ValueError(" ❌ Connection method required: either unix_socket or (host AND port)")

        if has_socket and has_tcp:
            logger.warning(" ⚠️ Both socket and TCP configuration provided, socket will be used")

    def get_connection_url(self) -> str:
        """
        Builds connection URL based on available parameters.
        Follows priority: Unix Socket > TCP
        """
        # Encode credentials
        user = quote_plus(self.username)
        pwd = quote_plus(self.password)
        db = quote_plus(self.database)

        # Base connection string
        url = f"postgresql://{user}:{pwd}@"

        # Add connection specific parts
        if self.unix_socket:
            url += f"/{db}?host={self.unix_socket}"
        else:
            url += f"{self.host}:{self.port}/{db}"

        return url

    @classmethod
    def from_env(cls, prefix: str = "POSTGRES_") -> "PostgresDSN":
        """Creates DSN from environment variables."""
        from os import getenv

        # Get environment variables
        config = {
            "username": getenv(f"{prefix}USER"),
            "password": getenv(f"{prefix}PASSWORD"),
            "database": getenv(f"{prefix}DB"),
            "host": getenv(f"{prefix}HOST"),
            "port": getenv(f"{prefix}PORT"),
            "unix_socket": getenv(f"{prefix}SOCKET")
        }

        # Convert port to integer if provided
        if config["port"]:
            try:
                config["port"] = int(config["port"])
            except ValueError:
                raise ValueError(f" ❌ Invalid port number: {config['port']}")

        # Create DSN instance
        try:
            return cls(**config)
        except ValueError as e:
            logger.error(f" ❌ Failed to create PostgreSQL DSN: {str(e)}")
            raise 