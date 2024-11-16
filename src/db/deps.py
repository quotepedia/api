from typing import Annotated, Any, Generator, Generic, TypeVar, cast

from fastapi import Depends
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session as BaseSession

from src.db import ENGINE

TQuery = TypeVar("TQuery", bound=Query[Any])


class GenericSession(BaseSession, Generic[TQuery]):
    def query(self, *args: Any, **kwargs: Any) -> TQuery:  # type: ignore
        return cast(TQuery, super().query(*args, **kwargs))


class GenericSessionFactory(Generic[TQuery]):
    def __init__(self, query_cls: type[TQuery] | None = None) -> None:
        self.query_cls = query_cls

    def __call__(self) -> Generator[GenericSession[TQuery], Any, None]:
        session: GenericSession[TQuery] = GenericSession(bind=ENGINE, query_cls=self.query_cls)

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


SessionDepends = Annotated[GenericSession[Query[Any]], Depends(GenericSessionFactory(Query[Any]))]
