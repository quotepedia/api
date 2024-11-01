from src.api.v1.users import me
from src.api.v1.users.deps import UserServiceDepends
from src.api.v1.users.models import User
from src.api.v1.users.routes import router
from src.api.v1.users.service import UserService

router.include_router(me.router)

__all__ = [
    "User",
    "UserService",
    "UserServiceDepends",
    "router",
]
