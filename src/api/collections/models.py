import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, object_session, relationship

from src.db.mixins import AuditMixin
from src.db.models import Base

if TYPE_CHECKING:
    from src.api.quotes import Quote
    from src.api.users import User


class QuoteCollection(Base):
    quote_id: Mapped[int] = mapped_column(ForeignKey("quote.id", ondelete="CASCADE"), primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id", ondelete="CASCADE"), primary_key=True)

    __repr_attrs__ = ("quote_id", "collection_id")


class Collection(Base, AuditMixin):
    class Visibility(enum.Enum):
        PUBLIC = enum.auto()
        PRIVATE = enum.auto()

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]] = mapped_column(index=True, default=None)
    emote: Mapped[Optional[str]] = mapped_column(index=True, default=None)
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), index=True, default=Visibility.PRIVATE)

    created_by_user: Mapped[Optional["User"]] = relationship(back_populates="collections")
    created_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), default=None)

    quotes: Mapped[list["Quote"]] = relationship(secondary="quote_collection", back_populates="collections")

    @property
    def quotes_count(self):
        from src.api.quotes import Quote

        session = object_session(self)
        return session.query(Quote).with_parent(self).count() if session else 0

    __repr_attrs__ = ("id", "name", "visibility")
