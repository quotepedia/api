from src.api.v1.users.schemas import UserResponse


class CurrentUserResponse(UserResponse):
    """Represents the public response data for a user."""

    id: int
    email: str
