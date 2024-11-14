from src.api.authors.deps import AuthorServiceDepends
from src.api.authors.models import Author
from src.api.authors.routes import router
from src.api.authors.service import AuthorService

__all__ = [
    "Author",
    "AuthorService",
    "AuthorServiceDepends",
    "router",
]
