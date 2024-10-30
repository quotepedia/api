from logging.config import dictConfig as configure_logging

from src.api.v1.authors import Author
from src.api.v1.collections import Collection, QuoteCollection
from src.api.v1.quotes import Quote
from src.api.v1.users import User
from src.config import settings

configure_logging(settings.logging)

__all__ = [
    "Author",
    "QuoteCollection",
    "Collection",
    "Quote",
    "User",
]
