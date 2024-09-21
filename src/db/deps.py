from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session as __Session

from src.db import ENGINE


def __get_session() -> Generator[__Session, None, None]:
    session = __Session(ENGINE)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


Session = Annotated[__Session, Depends(__get_session)]
