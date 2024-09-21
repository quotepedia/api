from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.config import settings


class UserEmail(BaseModel):
    """Represents user with email."""

    email: EmailStr = Field(max_length=255)


class UserPassword(BaseModel):
    """Represents user with password."""

    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    """Represents the public response data for a user."""

    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    avatar_url: str | None


class UserCreate(UserEmail, UserPassword):
    """Represents user registration details."""

    code: int = Field(ge=settings.otp.min, le=settings.otp.max)


class UserPasswordReset(UserEmail, UserPassword):
    """Represents user password reset details"""

    code: int = Field(ge=settings.otp.min, le=settings.otp.max)
