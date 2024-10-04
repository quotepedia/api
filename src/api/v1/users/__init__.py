from src.api.v1.users import me
from src.api.v1.users.routes import router

router.include_router(me.router)

__all__ = [
    "router",
]
