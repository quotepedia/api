from fastapi import APIRouter

from src.api.v1 import auth, authors, collections, media, otp, quotes, users

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth.router)
v1_router.include_router(authors.router)
v1_router.include_router(collections.router)
v1_router.include_router(media.router)
v1_router.include_router(otp.router)
v1_router.include_router(quotes.router)
v1_router.include_router(users.router)

__all__ = [
    "v1_router",
]
