from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status

from src.api.auth.deps import OAuth2BearerDepends, OptionalOAuth2BearerDepends
from src.api.auth.schemas import JWT
from src.api.users.models import User
from src.config import settings
from src.db.deps import SessionDepends


def get_current_user(session: SessionDepends, raw: OAuth2BearerDepends) -> User:
    try:
        data = JWT(**jwt.decode(raw, settings.jwt.secret, algorithms=[settings.jwt.algorithm]))
    except Exception:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Failed to verify credentials")

    user = session.get(User, data.sub)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if not user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Inactive user")
    return user


def get_current_user_or_none(session: SessionDepends, raw: OptionalOAuth2BearerDepends) -> User | None:
    return get_current_user(session, raw) if raw else None


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOrNone = Annotated[User | None, Depends(get_current_user_or_none)]
