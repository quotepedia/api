from datetime import datetime
from typing import Any, Callable

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.text import truncate


class ReprMixin:
    __repr_attrs__: tuple[str, ...] = tuple()

    __repr__formatters__: dict[type, Callable[[Any], str]] = {
        str: lambda value: f"'{truncate(value)}'",
    }

    def __repr__(self) -> str:
        attrs = map(self._format_attr, self.__repr_attrs__)
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def _format_attr(self, name: str) -> str:
        value = self._format_attr_value(getattr(self, name))
        return f"{name}={value}"

    def _format_attr_value(self, value: object) -> str:
        formatter = self._get_attr_formatter(type(value))
        return formatter(value) if formatter else str(value)

    def _get_attr_formatter(self, _type: type) -> Callable[[Any], str] | None:
        return self.__repr__formatters__.get(_type)


class AttributeUpdaterMixin:
    def update(self, args: dict[str, Any]) -> None:
        """Updates model attributes based on the provided args.

        Args:
            args (dict[str, Any]): A dictionary containing attribute names and their corresponding values.
        """

        for key, value in args.items():
            setattr(self, key, value)


class AuditMixin:
    """Provides automatic create and update timestamping."""

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
