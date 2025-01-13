import logging

from .config import settings

# Configure the base logging format and level
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance with the given name.

    :param str name: The name for the logger instance
    :return logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    return logger
