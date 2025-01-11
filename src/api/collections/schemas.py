from datetime import datetime
from typing import Annotated, Optional

from emoji import is_emoji
from pydantic import AfterValidator, BaseModel, Field, StringConstraints

from src.api.collections.models import Collection
from src.config import settings


def validate_emoji(value: str) -> str:
    assert is_emoji(value), f"Value '{value}' is not a valid emoji"
    return value


Emoji = Annotated[str, AfterValidator(validate_emoji), Field(examples=["😀"])]


class CollectionResponse(BaseModel):
    id: int
    name: str
    description: str
    emote: str
    visibility: Collection.Visibility
    quotes_count: int
    created_by_user_id: int
    created_at: datetime
    updated_at: datetime


CollectionName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.api.min_collection_name_length,
        max_length=settings.api.max_collection_name_length,
    ),
]

CollectionDescription = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=settings.api.max_collection_description_length,
    ),
]


class CollectionCreateRequest(BaseModel):
    name: CollectionName
    description: Optional[CollectionDescription] = None
    emote: Optional[Emoji] = None
    visibility: Collection.Visibility = Collection.Visibility.PRIVATE


class CollectionUpdateRequest(BaseModel):
    name: Optional[CollectionName] = None
    description: Optional[CollectionDescription] = None
    emote: Optional[Emoji] = None
    visibility: Optional[Collection.Visibility] = None
