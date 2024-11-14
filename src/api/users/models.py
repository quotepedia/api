from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixins import AuditMixin
from src.db.models import Base

if TYPE_CHECKING:
    from src.api.authors import Author
    from src.api.collections import Collection
    from src.api.quotes import Quote


class User(Base, AuditMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()
    avatar_url: Mapped[str | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    authors: Mapped[list["Author"]] = relationship(back_populates="created_by_user", cascade="all")

    quotes: Mapped[list["Quote"]] = relationship(back_populates="created_by_user", cascade="all")

    collections: Mapped[list["Collection"]] = relationship(back_populates="created_by_user", cascade="all")

    __repr_attrs__ = ("id",)
