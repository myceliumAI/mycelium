from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database.manager import db_manager


class DataContract(db_manager.Base):
    """
    Represents a Data Contract in the database.

    This model stores information about data contracts, including their specifications,
    metadata, and associated details. It maps to the 'data_contracts' table in the database.
    """

    __tablename__ = "data_contracts"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    data_contract_specification: Mapped[str] = mapped_column(String, nullable=False)
    info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    servers: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    terms: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    models: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    definitions: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    examples: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON)
    service_level: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    quality: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    links: Mapped[dict[str, str] | None] = mapped_column(JSON)
    tags: Mapped[list[str] | None] = mapped_column(JSON)

    def __repr__(self) -> str:
        """
        Returns a string representation of the DataContract object.
        :return str: A string representation of the DataContract object.
        """
        return f"<DataContract(id='{self.id}', title='{self.info.get('title', '')}', version='{self.info.get('version', '')}')>"
