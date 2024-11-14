from typing import Annotated

from pydantic import BaseModel, StringConstraints

from src.config import settings


class AuthorResponse(BaseModel):
    id: int
    name: str
    created_by_user_id: int | None


class AuthorCreateRequest(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=settings.api.min_author_name_length,
            max_length=settings.api.max_author_name_length,
        ),
    ]
