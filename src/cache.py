from typing import Any

from redis import Redis

from src.config import settings

redis = Redis(settings.redis.host)

CACHE_KEYS_SEPARATOR = ":"


def separate(*args: Any) -> str:
    return CACHE_KEYS_SEPARATOR.join(args)


__all__ = [
    "redis",
]
