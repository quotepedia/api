from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import Base

if TYPE_CHECKING:
    from src.api.v1.quotes import Quote
    from src.api.v1.users import User


class Author(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    created_by_user: Mapped[Optional["User"]] = relationship(back_populates="authors")
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), default=None)

    quotes: Mapped[list["Quote"]] = relationship(back_populates="author")

    __repr_attrs__ = ("id", "name")
