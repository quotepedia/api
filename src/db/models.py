from typing import Any

from pyheck import snake
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    @declared_attr
    @classmethod
    def __tablename__(cls) -> Any:
        return snake(cls.__name__)

    def update(self, schema: dict[str, Any]) -> None:
        """Updates model attributes based on the provided schema.

        Args:
            schema (dict[str, Any]): A dictionary containing attribute names and their corresponding values.
        """

        for key, value in schema.items():
            setattr(self, key, value)
