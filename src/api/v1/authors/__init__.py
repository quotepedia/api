from src.api.v1.authors.deps import AuthorServiceDepends
from src.api.v1.authors.models import Author
from src.api.v1.authors.routes import router
from src.api.v1.authors.service import AuthorService

__all__ = [
    "Author",
    "AuthorService",
    "AuthorServiceDepends",
    "router",
]
