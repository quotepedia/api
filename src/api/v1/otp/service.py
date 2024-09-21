from datetime import timedelta
from random import randint

from redis.typing import KeyT, ResponseT

from src.cache import redis, separate
from src.config import settings

__CACHE_KEY_PREFIX = "otp"


def set_otp(subject: KeyT) -> int:
    name = generate_otp_cache_name(subject)
    otp = generate_random_otp()
    expires_at = timedelta(minutes=settings.otp.expire_minutes)

    redis.set(name, otp, expires_at)

    return otp


def get_otp(subject: KeyT) -> ResponseT:
    name = generate_otp_cache_name(subject)
    otp = redis.get(name)

    return otp


def expire_otp(subject: KeyT) -> ResponseT:
    name = generate_otp_cache_name(subject)
    response = redis.delete(name)

    return response


def expire_otp_if_correct(subject: KeyT, otp: int) -> bool:
    is_correct = is_otp_correct(subject, otp)
    if is_correct:
        expire_otp(subject)
    return is_correct


def is_otp_correct(subject: KeyT, otp: int) -> bool:
    return get_otp(subject) == str(otp).encode()


def generate_random_otp() -> int:
    return randint(settings.otp.min, settings.otp.max)


def generate_otp_cache_name(subject: KeyT) -> KeyT:
    return separate(__CACHE_KEY_PREFIX, subject)
