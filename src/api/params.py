from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, StringConstraints

from src.config import settings

QQuery = Annotated[
    str | None,
    StringConstraints(
        min_length=1,
        max_length=255,
        strip_whitespace=True,
    ),
    Query(
        title="Search query",
        description="Search query string to filter results.",
    ),
]

SeedQuery = Annotated[
    float,
    Query(
        le=1.0,
        ge=-1.0,
        title="Random seed",
        description="Seed for random ordering in pagination.",
    ),
]

OffsetQuery = Annotated[
    int,
    Query(
        ge=0,
        title="Pagination offset",
        description="Number of results to skip for pagination.",
    ),
]

LimitQuery = Annotated[
    int,
    Query(
        ge=1,
        le=settings.api.max_search_params_limit,
        title="Pagination limit",
        description="Maximum number of results to return for pagination.",
    ),
]


class SearchParams(BaseModel):
    q: QQuery = None
    seed: SeedQuery = 0
    offset: OffsetQuery = 0
    limit: LimitQuery = settings.api.max_search_params_limit
