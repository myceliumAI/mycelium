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
    
    # Common options
    options: Optional[dict] = None

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
            # Unix socket connection (e.g., Cloud SQL)
            url += f"/{db}?host={self.unix_socket}"
        else:
            # TCP connection (default)
            host = self.host or 'localhost'
            port = self.port or 5432
            url += f"{host}:{port}/{db}"

        # Add additional options if provided
        if self.options:
            separator = '?' if '?' not in url else '&'
            options = '&'.join(f"{k}={quote_plus(str(v))}" for k, v in self.options.items())
            url += f"{separator}{options}"

        return url

    @classmethod
    def from_env(cls, prefix: str = "POSTGRES_") -> "PostgresDSN":
        """Creates DSN from environment variables."""
        from os import getenv

        # Required settings
        username = getenv(f"{prefix}USER")
        password = getenv(f"{prefix}PASSWORD")
        database = getenv(f"{prefix}DB")

        if not all([username, password, database]):
            raise ValueError(" ❌ Missing required database configuration")

        # Optional settings
        host = getenv(f"{prefix}HOST")
        port = getenv(f"{prefix}PORT")
        socket = getenv(f"{prefix}SOCKET")

        # Convert port to int if provided
        port = int(port) if port else None

        return cls(
            username=username,
            password=password,
            database=database,
            host=host,
            port=port,
            unix_socket=socket,
        ) 