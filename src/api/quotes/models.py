from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixins import AuditMixin
from src.db.models import Base

if TYPE_CHECKING:
    from src.api.authors import Author
    from src.api.collections import Collection
    from src.api.users import User


class Quote(Base, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(index=True)

    author: Mapped[Optional["Author"]] = relationship(back_populates="quotes")
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id", ondelete="SET NULL"), default=None)

    created_by_user: Mapped[Optional["User"]] = relationship(back_populates="quotes")
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), default=None)

    collections: Mapped[list["Collection"]] = relationship(secondary="quote_collection", back_populates="quotes")

    __repr_attrs__ = ("id", "content", "author_id", "created_by_user_id")
