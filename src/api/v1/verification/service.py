from datetime import timedelta
from random import randint

from redis.typing import KeyT, ResponseT

from src.cache import redis, separate
from src.config import settings

__CACHE_KEY_PREFIX = "codes"


def set_code(subject: KeyT) -> int:
    name = generate_code_cache_name(subject)
    code = generate_random_code()
    expires_at = timedelta(minutes=settings.otp.expire_minutes)

    redis.set(name, code, expires_at)

    return code


def get_code(subject: KeyT) -> ResponseT:
    name = generate_code_cache_name(subject)
    code = redis.get(name)

    return code


def expire_code(subject: KeyT) -> ResponseT:
    name = generate_code_cache_name(subject)
    response = redis.delete(name)

    return response


def expire_code_if_correct(subject: KeyT, code: int) -> bool:
    is_correct = is_code_correct(subject, code)
    if is_correct:
        expire_code(subject)
    return is_correct


def is_code_correct(subject: KeyT, code: int) -> bool:
    return get_code(subject) == str(code).encode()


def generate_random_code() -> int:
    return randint(settings.otp.min, settings.otp.max)


def generate_code_cache_name(subject: KeyT) -> KeyT:
    return separate(__CACHE_KEY_PREFIX, subject)
