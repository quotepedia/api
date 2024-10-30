from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import api_router
from src.config import settings
from src.i18n.deps import get_accept_language
from src.i18n.middleware import I18nMiddleware

app = FastAPI(
    debug=settings.debug,
    title=settings.app.name,
    version=settings.app.version,
    dependencies=[Depends(get_accept_language)],
    swagger_ui_parameters=settings.swagger_ui_parameters,
)

app.mount("/media", StaticFiles(directory=settings.path.media))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(I18nMiddleware)

app.include_router(api_router)
