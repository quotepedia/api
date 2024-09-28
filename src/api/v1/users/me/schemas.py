from src.api.v1.schemas import OTPRequest
from src.api.v1.users.schemas import UserEmailRequest, UserResponse


class CurrentUserResponse(UserResponse):
    """Represents the private response data for a user."""


class CurrentUserEmailUpdateRequest(UserEmailRequest, OTPRequest):
    """Represents a request to update current user's email."""
