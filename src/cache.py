from typing import Any

from redis import Redis

from src.config import settings

redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    ssl=settings.redis.ssl,
)

CACHE_KEYS_SEPARATOR = ":"


def separate(*args: Any) -> str:
    return CACHE_KEYS_SEPARATOR.join(args)


__all__ = [
    "redis",
]
