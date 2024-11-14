from logging.config import dictConfig as configure_logging

from src.api.authors import Author
from src.api.collections import Collection, QuoteCollection
from src.api.quotes import Quote
from src.api.users import User
from src.config import settings

configure_logging(settings.logging)

__all__ = [
    "Author",
    "QuoteCollection",
    "Collection",
    "Quote",
    "User",
]
