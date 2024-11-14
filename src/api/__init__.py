from fastapi import APIRouter

from src.api import auth, authors, collections, media, otp, quotes, users

router = APIRouter()

router.include_router(auth.router)
router.include_router(authors.router)
router.include_router(collections.router)
router.include_router(media.router)
router.include_router(otp.router)
router.include_router(quotes.router)
router.include_router(users.router)

__all__ = [
    "router",
]
