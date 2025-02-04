from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference

from src.api import router
from src.config import settings
from src.routing import generate_unique_route_id

app = FastAPI(
    debug=settings.debug,
    title=settings.app.name,
    version=settings.app.version,
    generate_unique_id_function=generate_unique_route_id,
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

app.include_router(router)


@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(title=app.title, openapi_url=app.openapi_url) if app.openapi_url else None
