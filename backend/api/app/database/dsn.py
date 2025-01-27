import logging
from dataclasses import dataclass
from urllib.parse import quote_plus

from ..errors.database.dsn import ConnectionMethodError, MissingCredentialsError
from ..utils.config import settings


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
    host: str | None = None
    port: int | None = None

    # Unix socket
    unix_socket: str | None = None

    # Additional connection options
    options: dict | None = None

    @classmethod
    def from_settings(cls) -> "PostgresDSN":
        """
        Creates a DSN instance from application settings.

        :return PostgresDSN: Configured database DSN
        """
        return cls(
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            unix_socket=settings.POSTGRES_SOCKET,
            options={},
        )

    def __post_init__(self):
        """
        Validate DSN configuration after initialization.
        Checks for required credentials and connection method.
        """
        # Initialize options if None
        if self.options is None:
            self.options = {}

        # Check credentials
        missing_credentials = []
        if not self.username:
            missing_credentials.append("username")
        if not self.password:
            missing_credentials.append("password")
        if not self.database:
            missing_credentials.append("database")

        if missing_credentials:
            raise MissingCredentialsError(missing_credentials)

        # Check connection method
        has_socket = bool(self.unix_socket)
        has_tcp = bool(self.host and self.port)

        if not has_socket and not has_tcp:
            raise ConnectionMethodError()

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
            logger.info(" ✅ Using Unix Socket")
            url += f"/{db}?host={self.unix_socket}"
        else:
            logger.info(" ✅ Using TCP")
            url += f"{self.host}:{self.port}/{db}"

        return url
