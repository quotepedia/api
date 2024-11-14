from pydantic import BaseModel

from src.api.v1.authors.schemas import AuthorResponse
from src.api.v1.collections.schemas import CollectionResponse
from src.api.v1.schemas import AuditResponse


class QuoteResponse(AuditResponse):
    id: int
    content: str
    created_by_user_id: int | None
    author: AuthorResponse | None


class QuoteCollectionsResponse(QuoteResponse):
    collections: list[CollectionResponse]


class QuoteCreateRequest(BaseModel):
    content: str
    author_id: int | None


class QuoteUpdateRequest(BaseModel):
    content: str | None = None
    author_id: int | None = None
