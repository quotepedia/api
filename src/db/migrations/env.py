from alembic import context
from sqlalchemy import create_engine

from src.config import settings
from src.db.models import Base


def run_migrations_offline() -> None:
    context.configure(url=str(settings.postgres.uri), target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(str(settings.postgres.uri))

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
