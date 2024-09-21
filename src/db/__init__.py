from sqlalchemy import create_engine

from src.config import settings

ENGINE = create_engine(str(settings.postgres.uri))
