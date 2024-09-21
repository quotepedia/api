from logging.config import dictConfig as configure_logging

from alembic import context
from sqlalchemy import create_engine

from src.api import *  # noqa: F403 https://github.com/sqlalchemy/alembic/issues/712
from src.config import settings
from src.db.models import Base

configure_logging(settings.logging)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """

    context.configure(
        url=str(settings.postgres.uri),
        target_metadata=Base.metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    engine = create_engine(str(settings.postgres.uri))

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
