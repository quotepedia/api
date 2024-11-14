from src.api.schemas import OTPRequest
from src.api.users.schemas import UserEmailRequest, UserResponse


class CurrentUserResponse(UserResponse):
    """Represents the private response data for a user."""


class CurrentUserEmailUpdateRequest(UserEmailRequest, OTPRequest):
    """Represents a request to update current user's email."""
