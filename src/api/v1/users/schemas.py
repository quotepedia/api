from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.api.v1.schemas import OTP


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


class UserCreate(UserEmail, UserPassword, OTP):
    """Represents user registration details."""


class UserPasswordReset(UserEmail, UserPassword, OTP):
    """Represents user password reset details"""
