from dataclasses import dataclass

from src.config import settings


@dataclass
class SearchParams:
    q: str | None = None
    offset: int = 0
    limit: int = settings.api.max_search_params_limit
