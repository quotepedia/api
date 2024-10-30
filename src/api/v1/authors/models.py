from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import Base

if TYPE_CHECKING:
    from src.api.v1.quotes import Quote


class Author(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    quotes: Mapped[list["Quote"]] = relationship(back_populates="author")

    __repr_attrs__ = ("id", "name")
