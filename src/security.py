from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.api.auth.schemas import JWT, AccessTokenResponse
from src.config import settings

__crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: int | str, minutes: int = settings.jwt.expire_minutes) -> AccessTokenResponse:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = JWT(exp=expires_at, sub=subject)
    access_token = jwt.encode(to_encode.model_dump(), settings.jwt.secret, algorithm=settings.jwt.algorithm)
    return AccessTokenResponse(access_token=access_token, expires_at=expires_at)


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return __crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return __crypt_context.hash(password)
