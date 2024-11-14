from typing import Annotated

from pydantic import BaseModel, EmailStr, SecretStr, StringConstraints

from src.api.schemas import AuditResponse, OTPRequest
from src.config import settings


class UserEmailRequest(BaseModel):
    """Represents a request containing a user's e-mail."""

    email: EmailStr


class UserPasswordRequest(BaseModel):
    """Represents a request containing a user's password."""

    password: Annotated[
        SecretStr,
        StringConstraints(
            min_length=settings.api.min_password_length,
            max_length=settings.api.max_password_length,
        ),
    ]


class UserPasswordResetRequest(UserEmailRequest, UserPasswordRequest, OTPRequest):
    """Represents a request for resetting a user's password."""


class UserRegistrationRequest(UserEmailRequest, UserPasswordRequest, OTPRequest):
    """Represents a request for user registration."""


class UserResponse(AuditResponse):
    """Represents the public response data for a user."""

    id: int
    email: str
    avatar_url: str | None
    is_active: bool
    is_verified: bool


class UserExistenceResponse(BaseModel):
    """Represents a response indicating whether a user exists."""

    exists: bool
